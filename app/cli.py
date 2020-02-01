import click
from flask import Flask

from app import db
from app.models import User


def register(app):
    @app.cli.command("create-admin")
    def create_admin():
        username = app.config["STATICE_USERNAME"]
        password = app.config["STATICE_PASSWORD"]
        if not User.query.filter_by(username=username).first():
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
