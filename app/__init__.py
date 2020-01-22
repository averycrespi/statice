from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    from app.dashboard import bp as dashboard_bp
    from app.settings import bp as settings_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(settings_bp)

    return app


from app import models
