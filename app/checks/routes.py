import arrow
from flask import abort, current_app, flash, redirect, render_template, url_for

from app import db
from app.models import Check, Event, Status
from app.checks import bp
from app.checks.forms import CreateCheckForm, DeleteCheckForm, EditCheckForm


@bp.route("/checks", methods=["GET", "POST"])
def checks():
    """Manage and create checks."""
    form = CreateCheckForm()
    if form.validate_on_submit():
        check = Check(name=form.name.data, url=form.url.data, status=Status.INFO,)
        db.session.add(check)
        db.session.flush()
        event = Event(
            check_id=check.id, message="Check has been created", status=Status.INFO,
        )
        db.session.add(event)
        db.session.commit()
        flash(f"Check {check.name} has been created.", category=Status.INFO)
        current_app.logger.info("created check: %s", check.name)
        return redirect(url_for("checks.checks"))
    return render_template("checks.html", checks=Check.query.all(), form=form)


@bp.route("/checks/<id>")
def view(id):
    """View a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    return render_template(
        "view_check.html",
        check=check,
        legend="Response Time (ms)",
        labels=[arrow.get(r.start_time).humanize() for r in check.responses[-10:]],
        values=[r.elapsed_ms for r in check.responses[-10:]],
    )


@bp.route("/checks/edit/<id>", methods=["GET", "POST"])
def edit(id):
    """Edit a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    form = EditCheckForm(obj=check)
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for("checks.checks"))
        check.name = form.name.data
        check.url = form.url.data
        db.session.add(check)
        db.session.commit()
        flash(f"Check {check.name} has been saved.", category=Status.INFO)
        current_app.logger.info("saved check: %s", check.name)
        return redirect(url_for("checks.checks"))
    return render_template("edit_check.html", form=form)


@bp.route("/checks/delete/<id>", methods=["GET", "POST"])
def delete(id):
    """Delete a check by ID."""
    check = Check.query.filter_by(id=id).first()
    if check is None:
        abort(404)
    form = DeleteCheckForm()
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect(url_for("checks.checks"))
        # TODO: implement cascade deletion
        db.session.delete(check)
        db.session.commit()
        flash(f"Check {check.name} has been deleted.", category=Status.WARNING)
        current_app.logger.warning("deleted check: %s", check.name)
        return redirect(url_for("checks.checks"))
    return render_template("delete_check.html", check=check, form=form)
