from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TimeField, PasswordField
from wtforms.validators import DataRequired, EqualTo


# import Models


class WaiterSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    waiter_name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField('Repeat Password')
    age = StringField('Age')
    phone = StringField('Phone')
    location = StringField('Location')
    job_name = StringField('Job Name', validators=[DataRequired()])
    auth = PasswordField('Auth', validators=[DataRequired()])
    submit = SubmitField('Submit')


class WaiterLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    waiter_name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
