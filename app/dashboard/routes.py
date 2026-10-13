from flask import Blueprint, render_template, redirect, url_for, session
from app.models import User, Scan

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

    recent_scans = all_scans[:5]  

    return render_template(
        "dashboard.html",
        user=user,
        total_scans=total_scans,
        safe_count=safe_count,
        suspicious_count=suspicious_count,
        phishing_count=phishing_count,
        recent_scans=recent_scans,
    )