from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError, URL

from app.models import Check


class CheckForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL()])
    interval = IntegerField(
        "Interval",
        description="Wait this many seconds between requests",
        default=15,
        validators=[DataRequired(), NumberRange(min=1)],
    )
    retries = IntegerField(
        "Retries",
        description="Retry this many times before reporting failure",
        default=3,
        validators=[DataRequired(), NumberRange(min=0)],
    )
    timeout = IntegerField(
        "Timeout",
        description="Stop waiting for a response after this many seconds",
        default=5,
        validators=[DataRequired(), NumberRange(min=1)],
    )


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
