from app import create_app
from app.config import Config
from app.daemon import Daemon


app = create_app(Config)


@app.cli.command("daemon")
def daemon():
    """Start the daemon."""
    daemon = Daemon()
    daemon.start()
