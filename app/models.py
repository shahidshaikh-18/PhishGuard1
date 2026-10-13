from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    scans = db.relationship("Scan", backref="user", lazy=True)


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    scan_type = db.Column(db.String(10), nullable=False)  # "url" or "file"

    url = db.Column(db.String(500), nullable=True)

    filename = db.Column(db.String(255), nullable=True)
    file_extension = db.Column(db.String(20), nullable=True)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    file_hash_sha256 = db.Column(db.String(64), nullable=True)

    risk_score = db.Column(db.Integer, nullable=False)
    classification = db.Column(db.String(20), nullable=False)
    indicators = db.Column(db.Text)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)