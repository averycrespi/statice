from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):  # type: ignore
    """Represents a (privileged) application user."""

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f"User({self.username}, {self.password_hash})"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Check(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
    status = db.Column(db.String())

    events = db.relationship("Event")
    responses = db.relationship("Response")

    def __repr__(self):
        return f"Check({self.name}, {self.url}, {self.status})"


class Event(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    message = db.Column(db.String())
    status = db.Column(db.String())

    def __lt__(self, other):
        # Sort events by timestamp.
        return self.time < other.time

    def __repr__(self):
        return f"Event({self.time}, {self.message}, {self.status})"


class Response(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    check_id = db.Column(db.Integer, db.ForeignKey("check.id"))

    start_time = db.Column(db.DateTime)
    elapsed_ms = db.Column(db.Integer)
    ok = db.Column(db.Boolean)
    description = db.Column(db.String())

    def __repr__(self):
        return f"Response({self.start_time}, {self.elapsed_ms}, {self.ok}, {self.description})"


class Status:
    INFO = "info"
    WARNING = "warning"
    FAILURE = "danger"
    SUCCESS = "success"


class Card:
    def __init__(self, check):
        self.check = check
        self.recent_events = sorted(check.events, reverse=True)[:3]
        self.table_data = None
