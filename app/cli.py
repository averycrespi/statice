from app import db


def register(app):
    @app.cli.group()
    def database():
        """Database commands."""

    @database.command()
    def create():
        """Create all tables."""
        db.create_all()

    @database.command()
    def drop():
        """Drop all tables."""
        db.drop_all()
