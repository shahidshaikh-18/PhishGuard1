from flask import Blueprint, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.dashboard.routes import current_user
from app import db

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
def view_profile():
    user = current_user()
    if not user:
        return redirect(url_for("auth.login"))

    message = None

    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not check_password_hash(user.password_hash, current_password):
            message = "Current password is incorrect."
        elif new_password != confirm_password:
            message = "New passwords do not match."
        elif len(new_password) < 8:
            message = "New password must be at least 8 characters."
        else:
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            message = "Password updated successfully."

    return render_template("profile.html", user=user, message=message)