import os


class Config:
    SITE_TITLE = os.environ.get("SITE_TITLE") or "Statice"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
