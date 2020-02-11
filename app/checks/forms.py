from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
    URL,
)

from app.checks.models import Check


class BaseCheckForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired(), URL(), Length(max=2048)],)


class CreateCheckForm(BaseCheckForm):
    submit = SubmitField("Create")

    def validate_name(self, name):
        if Check.query.filter_by(name=name.data).first() is not None:
            raise ValidationError("Please enter a unique name.")


class EditCheckForm(BaseCheckForm):
    submit = SubmitField("Save")
    cancel = SubmitField("Cancel")


class DeleteCheckForm(FlaskForm):
    submit = SubmitField("Delete")
    cancel = SubmitField("Cancel")
