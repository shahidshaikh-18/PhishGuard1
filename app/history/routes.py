from flask import Blueprint, request, render_template, redirect, url_for
from app.models import Scan
from app.dashboard.routes import current_user
from app import db

history_bp = Blueprint("history", __name__)

PER_PAGE = 10


@history_bp.route("/history")
def scan_history():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    search_query = request.args.get("q", "").strip()
    classification_filter = request.args.get("classification", "")
    sort = request.args.get("sort", "date_desc")
    page = request.args.get("page", 1, type=int)

    query = Scan.query.filter_by(user_id=user.id)

    if search_query:
        query = query.filter(
            (Scan.url.ilike(f"%{search_query}%")) | (Scan.filename.ilike(f"%{search_query}%"))
        )

    if classification_filter:
        query = query.filter_by(classification=classification_filter)

    if sort == "date_asc":
        query = query.order_by(Scan.scanned_at.asc())
    elif sort == "risk_desc":
        query = query.order_by(Scan.risk_score.desc())
    elif sort == "risk_asc":
        query = query.order_by(Scan.risk_score.asc())
    else:
        query = query.order_by(Scan.scanned_at.desc())

    pagination = query.paginate(page=page, per_page=PER_PAGE, error_out=False)

    return render_template(
        "history.html",
        scans=pagination.items,
        pagination=pagination,
        search_query=search_query,
        classification_filter=classification_filter,
        sort=sort,
    )


@history_bp.route("/history/delete/<int:scan_id>", methods=["POST"])
def delete_scan(scan_id):
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    scan = Scan.query.filter_by(id=scan_id, user_id=user.id).first()
    if scan:
        db.session.delete(scan)
        db.session.commit()

    return redirect(url_for("history.scan_history"))


@history_bp.route("/insights")
def insights():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    all_scans = Scan.query.filter_by(user_id=user.id).order_by(Scan.scanned_at.asc()).all()

    # Data for the doughnut chart: count per classification
    safe_count = sum(1 for s in all_scans if s.classification == "Safe")
    suspicious_count = sum(1 for s in all_scans if s.classification == "Suspicious")
    high_risk_count = sum(1 for s in all_scans if s.classification == "High Risk")

    # Data for the line chart: scans per day (last 14 entries' dates, simple version)
    chart_labels = [s.scanned_at.strftime("%d %b") for s in all_scans[-14:]]
    chart_scores = [s.risk_score for s in all_scans[-14:]]

    return render_template(
        "insights.html",
        safe_count=safe_count,
        suspicious_count=suspicious_count,
        high_risk_count=high_risk_count,
        chart_labels=chart_labels,
        chart_scores=chart_scores,
    )