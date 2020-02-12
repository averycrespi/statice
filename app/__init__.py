from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy
import logging


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
rq = RQ()


def create_app(config_class):
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.setLevel(logging.INFO)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    rq.init_app(app)

    from app.admin import bp as admin_bp
    from app.dashboard import bp as dashboard_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)

    from app.errors import page_not_found

    app.register_error_handler(404, page_not_found)

    with app.app_context():
        db.create_all()

    return app
