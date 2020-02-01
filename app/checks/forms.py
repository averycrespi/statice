from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    ValidationError,
    URL,
)

from app.models import Check


class CheckForm(FlaskForm):
    """Base class for creating or editing a check."""

    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])


class CreateCheckForm(CheckForm):
    submit = SubmitField("Create")

    def validate_name(self, name):
        if Check.query.filter_by(name=name.data).first() is not None:
            raise ValidationError("Please use a unique check name.")


class EditCheckForm(CheckForm):
    submit = SubmitField("Save")
    cancel = SubmitField("Cancel")


class DeleteCheckForm(FlaskForm):
    submit = SubmitField("Delete")
    cancel = SubmitField("Cancel")
