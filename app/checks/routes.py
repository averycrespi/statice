from flask import flash, redirect, render_template, url_for

from app import db
from app.models import Category, Check, Event, Response
from app.checks import bp
from app.checks.forms import CreateCheckForm, DeleteCheckForm


@bp.route("/checks", methods=["GET", "POST"])
def checks():
    form = CreateCheckForm()
    if form.validate_on_submit():
        check = Check(
            name=form.name.data,
            url=form.url.data,
            status=Category.INFO,
            interval=form.interval.data,
            retries=form.retries.data,
            timeout=form.timeout.data,
        )
        db.session.add(check)
        db.session.flush()
        event = Event(
            check_id=check.id, message="Check has been created", category=Category.INFO,
        )
        db.session.add(event)
        db.session.commit()
        flash(f"Check {check.name} has been created.", category=Category.INFO)
        return redirect(url_for("checks.checks"))
    return render_template("checks.html", checks=Check.query.all(), form=form)


@bp.route("/checks/edit/<id>", methods=["GET", "POST"])
def edit(id):
    return render_template("edit_check.html")


@bp.route("/checks/delete/<id>", methods=["GET", "POST"])
def delete(id):
    check = Check.query.filter_by(id=id).first()
    if check is None:
        return render_template("404.html")
    form = DeleteCheckForm()
    if form.validate_on_submit():
        # TODO: implement cascade deletion
        db.session.delete(check)
        db.session.commit()
        flash(f"Check {check.name} has been deleted.", category=Category.INFO)
        return redirect(url_for("checks.checks"))
    return render_template("delete_check.html", check=check, form=form)
