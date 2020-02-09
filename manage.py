from app import create_app, db
from app.config import DevConfig
from app.daemons.inquisitor import Inquisitor
from app.daemons.janitor import Janitor
from app.models import User


app = create_app(DevConfig)


@app.cli.command("create_user")
def create_user():
    """Create the default user."""
    username = app.config["STATICE_ADMIN_USERNAME"]
    password = app.config["STATICE_ADMIN_PASSWORD"]
    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(password)
        app.logger.info("Updated existing user: %s", username)
    else:
        user = User(username=username)
        user.set_password(password)
        app.logger.info("Created admin user: %s", username)
    db.session.add(user)
    db.session.commit()


@app.cli.command("inquisitor")
def inquisitor():
    """Run the inquisitor."""
    inquisitor = Inquisitor(
        interval=app.config["STATICE_REQUEST_INTERVAL"],
        timeout=app.config["STATICE_REQUEST_TIMEOUT"],
    )
    inquisitor.run()


@app.cli.command("janitor")
def janitor():
    """Run the janitor."""
    janitor = Janitor(
        interval=app.config["STATICE_PURGE_INTERVAL"],
        age=app.config["STATICE_PURGE_AGE"],
    )
    janitor.run()
