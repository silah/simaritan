from datetime import datetime

from simaritan import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    name = db.Column(db.String(32), index=True)
    email = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.String(64), index=True)
    team = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Incident(db.Model):
    id = db.Column(db.Integer)
    incident_no = db.Column(db.String(32), primary_key=True, index=True, unique=True)
    description = db.Column(db.String(512))
    # DB relationship with tasks and events, backreference to incident number
    tasks = db.relationship('Task', backref='incidentno', lazy='dynamic')
    events = db.relationship('Event', backref='incidentno', lazy='dynamic')
    impactstatement = db.relationship('ImpactStatement', backref='incidentno', lazy='dynamic')


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
    # assignee = db.Column(db.String(32), index=True, ForeignKey='User.username')


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(512))
    assignee = db.Column(db.String(32), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    incident_no = db.Column(db.String(32), db.ForeignKey('incident.incident_no'), index=True)

    def __repr__(self):
        return 'Body {}'.format(self.body)