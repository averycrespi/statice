import os


class Config:
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME") or "admin"
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") or "admin"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite://"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
