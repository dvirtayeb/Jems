from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class WaiterForm(FlaskForm):
    waiter_name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age')
    phone = StringField('Phone')
    location = StringField('Location')
    job_name = StringField('Job_name')
    submit = SubmitField('Submit', )
