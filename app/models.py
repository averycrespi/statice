from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):  # type: ignore
    """Represents a (privileged) application user."""

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Check(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.String())
    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())

    events = db.relationship("Event")
    responses = db.relationship("Response")


class Event(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    status = db.Column(db.String())
    message = db.Column(db.String())
    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __lt__(self, other):
        # Sort events by timestamp.
        return self.time < other.time


class Response(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status_code = db.Column(db.Integer)


class Status:
    INFO = "info"
    WARNING = "warning"
    FAILURE = "danger"
    SUCCESS = "success"
