from app import db


class OutboundCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    url = db.Column(db.String())
