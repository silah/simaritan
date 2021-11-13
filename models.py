from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from simaritan import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.String(64), index=True)
    team = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# User Loader function sets the user session, so user remains logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Incident(db.Model):
    id = db.Column(db.Integer)
    incident_no = db.Column(db.String(32), primary_key=True, index=True, unique=True)
    description = db.Column(db.String(512))
    status = db.Column(db.String(32))
    inc_mgr = db.Column(db.Integer, index=True)
    start_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # DB relationship with tasks and events, backreference to incident number
    tasks = db.relationship('Task', backref='incidentno', lazy='dynamic')
    events = db.relationship('Event', backref='incidentno', lazy='dynamic')
    impactstatement = db.relationship('ImpactStatement', backref='incidentno', lazy='dynamic')
    incidentteam = db.relationship('IncMem', backref='incidentno', lazy='dynamic')


class ImpactStatement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)
    # incident_no = db.Column(db.String(32), primary_key=True, ForeignKey='Incident.incident_no', index=True,
    # unique=True)
    body = db.Column(db.String(512))
    submitter = db.Column(db.String(32), index=True)
    # submitter = db.Column(db.String(32), index=True, ForeignKey='User.username')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)
    body = db.Column(db.String(512))
    assignee = db.Column(db.String(32), index=True)
    eta = db.Column(db.String(32))
    status = db.Column(db.String(32))
    # assignee = db.Column(db.String(32), index=True, ForeignKey='User.username')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    assignee = db.Column(db.String(32), index=True)
    activity = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)

    def __repr__(self):
        return 'Body {}'.format(self.body)


class IncMem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person = db.Column(db.String(512), index=True)
    role = db.Column(db.String(32), index=True)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)

    def __repr__(self):
        return 'Person {}'.format(self.person)


class system(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64), index=True)
    owner = db.Column(db.String(64), index=True)
    primary_contact = db.Column(db.String(64), index=True)
    contact_number = db.Column(db.String(64), index=True)
    contact_email = db.Column(db.String(64), index=True)


class system_inc_rel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)
    sysid = db.Column(db.Integer, db.ForeignKey('system.id'))
