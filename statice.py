from app import create_app
from app.cli import register


app = create_app()
register(app)
