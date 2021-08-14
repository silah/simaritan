from simaritan import app, db
from flask import render_template, flash, redirect
from simaritan.forms import LoginForm, TaskAdditionForm, EventAdditionForm, PersonAdditionForm, ImpactStatementForm, \
    IncidentStart
from models import Incident, IncMem, ImpactStatement, Task, Event


@app.route('/')
@app.route('/index')
def index():
    loggedin = False
    if loggedin:
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect('/index')
    else:
        return render_template('login.html', title='Log in', form=form)


@app.route('/overview', methods=['GET', 'POST'])
def overview():
    user = {'username': 'Silas', 'id': 1}
    incf = IncidentStart()
    users_incidents = Incident.query.filter_by(inc_mgr=user.id).all()

    if incf.validate_on_submit():
        incident = Incident(incident_no=incf.inc_no.data, description=incf.description.data,
                            status='Open', inc_mgr=user.id)
        event = Event(body='Incident Opened: {}'.format(incf.inc_no.data), assignee=user.username,
                      activity='Incident Started', incident_no=incf.incident_no)
        db.session.add(incident)
        db.session.add(event)
        db.session.commit()

        return redirect('/admin/{}'.format(incf.inc_no.data))

    return render_template('startIncident.html', incf=incf, incs=users_incidents)

@app.route('/dashboard/<incident>')
def dashboard(incident):
    user = {'username': 'Silas', 'id': 1}
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    return render_template('dashboard.html', title='Incident Dashboard', user=user, tasks=tasks, team=team,
                           timeline=timeline,
                           impacts=impacts, inc=inc)


@app.route('/dashboard')
def dashboard_blank():
    return "You have not selected an Incident"


@app.route('/admin')
def admin_blank():
    return "You have not selected an Incident"


@app.route('/admin/<incident>', methods=['GET', 'POST'])
def admin(incident):
    taskform = TaskAdditionForm()
    eventform = EventAdditionForm()
    personform = PersonAdditionForm()
    user = {'username': 'Silas'}
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    if taskform.validate_on_submit():
        task = Task(incident_no=inc.incident_no, body=taskform.task.data, assignee=taskform.owner.data,
                    eta=taskform.eta.data, status=taskform.already_done.data)
        event = Event(body=taskform.task.data, assignee=taskform.owner.data, activity='Task Added',
                      incident_no=inc.incident_no)
        db.session.add(task)
        db.session.add(event)
        db.session.commit()

        flash('Task added: {} assigned to {}'.format(
            taskform.task.data, taskform.owner.data
        ))
        tasks = Task.query.filter_by(incident_no=incident).all()
        timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
        return render_template('admin.html', title='Admin', taskf=taskform, eventf=eventform, teamf=personform,
                               user=user, tasks=tasks, impacts=impacts, inc=inc, team=team, timeline=timeline)
    elif eventform.validate_on_submit():

        event = Event(body=eventform.event.data, assignee=eventform.owner.data, activity=eventform.activity_type.data,
                      incident_no=inc.incident_no)

        db.session.add(event)
        db.session.commit()

        flash('Event added: {} by {}'.format(
            eventform.event.data, eventform.owner.data
        ))
        timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
        return render_template('admin.html', title='Admin', taskf=taskform, eventf=eventform, teamf=personform,
                               user=user, tasks=tasks, impacts=impacts, inc=inc, team=team, timeline=timeline)
    elif personform.validate_on_submit():
        prson = IncMem(incident_no=inc.incident_no, person=personform.person.data, role=personform.role.data)
        event = Event(body='{}, {} - Joined the incident team'.format(personform.person.data, personform.role.data),
                      assignee=personform.role.data, activity='Person joined',
                      incident_no=inc.incident_no)
        db.session.add(prson)
        db.session.add(event)
        db.session.commit()

        flash('{}, {} - Joined the incident team'.format(personform.person.data, personform.role.data))
        timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
        team = IncMem.query.filter_by(incident_no=incident).all()
        return render_template('admin.html', title='Admin', taskf=taskform, eventf=eventform, teamf=personform,
                               user=user, tasks=tasks, impacts=impacts, inc=inc, team=team, timeline=timeline)
    else:
        return render_template('admin.html', title='Admin', taskf=taskform, eventf=eventform, teamf=personform,
                               user=user, tasks=tasks, impacts=impacts, inc=inc, team=team, timeline=timeline)


@app.route('/submitimpact/<incident>', methods=['GET', 'POST'])
def submitimpact(incident):
    form = ImpactStatementForm()
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()

    if form.validate_on_submit():
        sttmnt = ImpactStatement(incident_no=inc.incident_no, body=form.statement.data, submitter=form.submitter.data)
        event = Event(body=form.statement.data, assignee=form.submitter.data, activity='Impact added',
                      incident_no=inc.incident_no)
        db.session.add(sttmnt)
        db.session.add(event)
        db.session.commit()

        flash('Statement added: {} by {}'.format(
            form.statement.data, form.submitter.data
        ))
        impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
        return render_template('submitImpact.html', title='Submit Impact Statement for {}'.format(inc.incident_no),
                               impacts=impacts, inc=inc, impactf=form)
    else:
        return render_template('submitImpact.html', title='Submit Impact Statement for {}'.format(inc.incident_no),
                               impacts=impacts, inc=inc, impactf=form)
