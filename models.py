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


class ImpactStatement(db.Model):
    id = db.Column(db.Integer)
    incident_no = db.Column(db.String(32), primary_key=True, index=True, unique=True)
    # incident_no = db.Column(db.String(32), primary_key=True, ForeignKey='Incident.incident_no', index=True,
    # unique=True)
    description = db.Column(db.String(512))
    submitter = db.Column(db.String(32), index=True)
    # submitter = db.Column(db.String(32), index=True, ForeignKey='User.username')


class Task(db.Model):
    id = db.Column(db.Integer)
    incident_no = db.Column(db.String(32), primary_key=True, index=True, unique=True)
    # incident_no = db.Column(db.String(32), primary_key=True, ForeignKey='Incident.incident_no', index=True,
    # unique=True)
    description = db.Column(db.String(512))
    assignee = db.Column(db.String(32), index=True)
    # assignee = db.Column(db.String(32), index=True, ForeignKey='User.username')
