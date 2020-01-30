from app import create_app, db
from app.models import User


app = create_app()
with app.app_context():
    username, password = app.config["ADMIN_USERNAME"], app.config["ADMIN_PASSWORD"]
    if not User.query.filter_by(username=username).first():
        admin = User(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

#TODO: remove me!
from pprint import pprint
pprint(app.config)
