from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.checks import bp as checks_bp
    from app.dashboard import bp as dashboard_bp

    app.register_blueprint(checks_bp, url_prefix="/checks")
    app.register_blueprint(dashboard_bp)

    return app


from app import models
