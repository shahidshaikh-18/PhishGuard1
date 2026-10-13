from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from flask import Blueprint, render_template, redirect, url_for, session
from app.models import User, Scan

auth_bp = Blueprint("auth", __name__)

dashboard_bp = Blueprint("dashboard", __name__)


def current_user():
    """Helper: returns the logged-in User object, or None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


@dashboard_bp.route("/dashboard")
def overview():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    all_scans = Scan.query.filter_by(user_id=user.id).order_by(Scan.scanned_at.desc()).all()

    total_scans = len(all_scans)
    safe_count = sum(1 for s in all_scans if s.classification == "Safe")
    suspicious_count = sum(1 for s in all_scans if s.classification == "Suspicious")
    phishing_count = sum(1 for s in all_scans if s.classification == "High Risk")

    recent_scans = all_scans[:5]  # most recent 5, since we already sorted newest-first

    return render_template(
        "dashboard.html",
        user=user,
        total_scans=total_scans,
        safe_count=safe_count,
        suspicious_count=suspicious_count,
        phishing_count=phishing_count,
        recent_scans=recent_scans,
    )


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("signup.html", message="Passwords do not match.")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("signup.html", message="An account with this email already exists.")

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("dashboard.overview"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            remember = request.form.get("remember")
            session.permanent = True if remember == "on" else False
            session["user_id"] = user.id
            return redirect(url_for("dashboard.overview"))
        else:
            return render_template("login.html", message="Invalid email or password.")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))