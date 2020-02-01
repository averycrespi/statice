from app import create_app, db
from app.models import User


app = create_app()
with app.app_context():
    # TODO: Move to CLI script (create_admin)
    username = app.config["STATICE_USERNAME"]
    if not User.query.filter_by(username=username).first():
        admin = User(username=username)
        admin.set_password(app.config["STATICE_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
