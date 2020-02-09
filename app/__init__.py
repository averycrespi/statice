from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy

from app.handlers import page_not_found


bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
migrate = Migrate()
moment = Moment()
rq = RQ()


def create_app(config):
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    rq.init_app(app)

    from app.auth import bp as auth_bp
    from app.checks import bp as checks_bp
    from app.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(checks_bp)
    app.register_blueprint(main_bp)

    app.register_error_handler(404, page_not_found)

    with app.app_context():
        db.create_all()

    return app


from app import models


@login.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()
