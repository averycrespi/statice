import os


class Config:
    STATICE_USERNAME = os.environ.get("STATICE_USERNAME") or "admin"
    STATICE_PASSWORD = os.environ.get("STATICE_PASSWORD") or "admin"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "change-me"

    POSTGRES_URL = os.environ.get("POSTGRES_URL") or "localhost:5432"
    POSTGRES_DB = os.environ.get("POSTGRES_DB") or "postgres"
    POSTGRES_USER = os.environ.get("POSTGRES_USER") or "postgres"
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD") or "postgres"

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{user}:{pw}@{url}/{db}".format(
        user=POSTGRES_USER, pw=POSTGRES_PASSWORD, url=POSTGRES_URL, db=POSTGRES_DB
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
