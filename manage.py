from app import create_app
from app.config import Config
from app.tasks import Inquisitor, Janitor


app = create_app(Config)


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
