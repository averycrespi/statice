from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_rq2 import RQ
from flask_sqlalchemy import SQLAlchemy


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()
rq = RQ()


def page_not_found(e):
    """Handle 404 error."""
    return render_template("404.html"), 404


def create_app(config):
    """Create an application instance."""
    app = Flask(__name__)
    app.config.from_object(config)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    rq.init_app(app)

    from app.checks import bp as checks_bp
    from app.dashboard import bp as dashboard_bp

    app.register_blueprint(checks_bp)
    app.register_blueprint(dashboard_bp)

    app.register_error_handler(404, page_not_found)

    with app.app_context():
        db.create_all()

    return app


from app import models
