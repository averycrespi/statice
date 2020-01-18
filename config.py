import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"
    DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite://"
