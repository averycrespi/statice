from app import create_app, db
from app.models import Check, Event


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Check": Check, "Event": Event}
