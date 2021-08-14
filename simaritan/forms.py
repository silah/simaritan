from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TimeField, HiddenField
from wtforms.validators import DataRequired
#from datetime import datetime
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class TaskAdditionForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    eta = StringField('ETA (HH:MM)', validators=[DataRequired()])
    already_done = BooleanField('Already completed')
    submit = SubmitField('Add Task')


class EventAdditionForm(FlaskForm):
    event = StringField('Event', validators=[DataRequired()])
    owner = StringField('Owner', validators=[DataRequired()])
    activity_type = StringField('Activity type', validators=[DataRequired()])
    # eta = TimeField('Time', format='%H:%M', default=datetime.now(), validators=[DataRequired()])
    submit = SubmitField('Add Event')


class PersonAdditionForm(FlaskForm):
    person = StringField('Name', validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Add Person')


class ImpactStatementForm(FlaskForm):
    statement = StringField('Impact Statement', validators=[DataRequired()])
    submitter = StringField('Submitter', validators=[DataRequired()])
    submit = SubmitField('Submit Impact Statement')


class IncidentStart(FlaskForm):
    inc_no = StringField('Incident Number', validators=[DataRequired()])
    description = StringField('Incident Description', widget=TextArea(), validators=[DataRequired()])
    inc_mgr = StringField('Incident Manager', validators=[DataRequired()])
    submit = SubmitField('Initiate incident')
