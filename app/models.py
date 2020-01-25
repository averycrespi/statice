from datetime import datetime

from app import db


class Check(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
