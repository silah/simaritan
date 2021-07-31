from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class TaskAdditionForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    eta = TimeField('ETA', validators=[DataRequired()])
    already_done = BooleanField('Already completed')
    submit = SubmitField('Add Task')


class EventAdditionForm(FlaskForm):
    event = StringField('Event', validators=[DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    eta = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Add Event')


class PersonAdditionForm(FlaskForm):
    person = StringField('Name', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Add Person')
