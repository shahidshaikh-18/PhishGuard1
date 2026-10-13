from flask import Blueprint, request, render_template, redirect, url_for, session
from app.models import User, Scan
from app.dashboard.routes import current_user
from app.scanner.engine import analyze_url, analyze_file
from app import db
import hashlib
import os
from werkzeug.utils import secure_filename

scanner_bp = Blueprint("scanner", __name__)


@scanner_bp.route("/scan", methods=["GET", "POST"])
def scan_url():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    result = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url.startswith(("http://", "https://")):
            return render_template("scanner.html", message="Enter a valid URL starting with http:// or https://")

        score, classification, indicators = analyze_url(url)

        new_scan = Scan(
            user_id=user.id,
            scan_type="url",
            url=url,
            risk_score=score,
            classification=classification,
            indicators="|".join(indicators),
        )
        db.session.add(new_scan)
        db.session.commit()

        return redirect(url_for("scanner.scan_result", scan_id=new_scan.id))

    return render_template("scanner.html", result=result)


@scanner_bp.route("/scan/<int:scan_id>")
def scan_result(scan_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    scan = Scan.query.filter_by(id=scan_id, user_id=user.id).first()
    if not scan:
        return redirect(url_for("dashboard.overview"))

    indicator_list = scan.indicators.split("|") if scan.indicators else []

    return render_template("scan_result.html", scan=scan, indicators=indicator_list)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB limit, keeps this safe and simple


@scanner_bp.route("/scan/file", methods=["GET", "POST"])
def scan_file():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            return render_template("scan_file.html", message="Please choose a file to scan.")

        filename = secure_filename(uploaded_file.filename)

        file_bytes = uploaded_file.read()
        file_size = len(file_bytes)

        if file_size > MAX_FILE_SIZE:
            return render_template("scan_file.html", message="File too large. Maximum size is 10 MB.")

        file_hash = hashlib.sha256(file_bytes).hexdigest()

        score, classification, indicators = analyze_file(filename, file_size, file_hash)

        new_scan = Scan(
            user_id=user.id,
            scan_type="file",
            filename=filename,
            file_extension=os.path.splitext(filename)[1],
            file_size_bytes=file_size,
            file_hash_sha256=file_hash,
            risk_score=score,
            classification=classification,
            indicators="|".join(indicators),
        )
        db.session.add(new_scan)
        db.session.commit()

        return redirect(url_for("scanner.scan_result", scan_id=new_scan.id))

    return render_template("scan_file.html")