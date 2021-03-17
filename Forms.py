from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TimeField
from wtforms.validators import DataRequired

# import Models


class WaiterForm(FlaskForm):
    waiter_name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age')
    phone = StringField('Phone')
    location = StringField('Location')
    job_name = StringField('Job Name', validators=[DataRequired()])
    submit = SubmitField('Submit', )
