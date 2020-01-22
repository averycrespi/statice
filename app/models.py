from datetime import datetime

from app import db


class Check(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())


class Event(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
