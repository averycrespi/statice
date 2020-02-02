from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config):
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from app.dashboard import bp as dashboard_bp
    from app.checks import bp as checks_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(checks_bp)

    with app.app_context():
        db.create_all()

    return app


from app import models
