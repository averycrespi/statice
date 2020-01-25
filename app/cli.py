import click
from faker import Faker
import faker.providers.lorem
import faker.providers.internet

from app import db
from app.models import Check, Event, Response, User


def register(app):
    @app.cli.command("fake")
    @click.argument("count", default=5)
    def fake(count):
        """Add fake data."""
        faker = Faker()
        categories = ("success", "warning", "danger", "info")
        for i in range(count):
            print("Faking data ...")
            check = Check(
                name=faker.word().title(),
                url=faker.uri(),
                status=faker.random_element(categories),
                period=faker.random_int(min=1, max=60),
                retries=faker.random_int(min=0, max=5),
                timeout=faker.random_int(min=3, max=10),
            )
            db.session.add(check)
            db.session.flush()  # Ensure that check.id is up-to-date.
            event = Event(
                check_id=check.id,
                category=faker.random_element(categories),
                message=faker.sentence(),
            )
            db.session.add(event)
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
