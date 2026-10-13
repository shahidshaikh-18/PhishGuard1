from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from datetime import timedelta

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.permanent_session_lifetime = timedelta(days=7)

    db.init_app(app)

    with app.app_context():
        from app import models
        db.create_all()

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from app.scanner.routes import scanner_bp
    app.register_blueprint(scanner_bp)

    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)

    from app.history.routes import history_bp
    app.register_blueprint(history_bp)

    @app.route("/")
    def home():
        return redirect(url_for("auth.signup"))

    return app