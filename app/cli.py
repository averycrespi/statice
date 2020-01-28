import click
from faker import Faker

from app import db
from app.fake import fake_check, fake_event
from app.models import User


def register(app):
    @app.cli.command("fake")
    @click.argument("count", default=5)
    def fake(count):
        """Add fake data."""
        faker = Faker()
        print("Faking data ...")
        for i in range(count):
            check = fake_check(faker)
            db.session.add(check)
            db.session.flush()  # Ensure that check.id is up-to-date.
            for i in range(faker.random_int(min=0, max=4)):
                db.session.add(fake_event(faker, check))
        print("Committing changes ...")
        db.session.commit()
        print("Done!")

    @app.cli.command("reset")
    def reset():
        """Reset the database."""
        print("Dropping all tables ...")
        db.drop_all()
        print("Creating all tables ...")
        db.create_all()
        print("Adding admin user ...")
        admin = User(username=app.config["ADMIN_USERNAME"])
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)
        print("Committing changes ...")
        db.session.commit()
        print("Done!")
