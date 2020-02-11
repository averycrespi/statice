from app import create_app
from app.background import Daemon
from app.config import Config


app = create_app(Config)


@app.cli.command("daemon")
def daemon():
    """Start the daemon."""
    daemon = Daemon()
    daemon.start()
