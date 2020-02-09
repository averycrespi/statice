from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth.forms import LoginForm
from app.models import Status, User


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user."""
    form = LoginForm()
    if form.validate_on_submit():
        username = current_app.config["STATICE_ADMIN_USERNAME"]
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.", category=Status.FAILURE)
            return redirect(url_for("auth.login"))
        login_user(user, remember=True)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.dashboard")
        return redirect(next_page)
    return render_template("login.j2", form=form)
