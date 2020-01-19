from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import OutboundCheck


class CreateOutboundCheckForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    submit = SubmitField("Create")

    def validate_name(self, name):
        if OutboundCheck.query.filter_by(name=name.data).first():
            raise ValidationError("Please use a different name.")


class DeleteOutboundCheckForm(FlaskForm):
    delete = SubmitField("Delete")
