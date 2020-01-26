from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app.models import Check


class CreateCheckForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
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
    submit = SubmitField("Create")

    def validate_name(self, name):
        if Check.query.filter_by(name=name.data).first() is not None:
            raise ValidationError("Please use a unique check name.")
