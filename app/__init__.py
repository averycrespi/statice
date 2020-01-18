from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config


bootstrap = Bootstrap()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)

    from app.core import bp as core_bp

    app.register_blueprint(core_bp)

    return app
