from simaritan import app, db
from flask import render_template, flash, redirect
from simaritan.forms import LoginForm, TaskAdditionForm, EventAdditionForm, PersonAdditionForm, ImpactStatementForm
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


@app.route('/dashboard/<incident>')
def dashboard(incident):
    user = {'username': 'Silas'}
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    timeline = Event.query.filter_by(incident_no=incident).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    return render_template('dashboard.html', title='Incident Dashboard', user=user, tasks=tasks, team=team, timeline=timeline,
                    impacts=impacts, inc=inc)


@app.route('/dashboard')
def dashboard_blank():
    return "You have not selected an Incident"


@app.route('/admin')
def admin_blank():
    return "You have not selected an Incident"


@app.route('/admin/<incident>')
def admin(incident):
    taskform = TaskAdditionForm()
    eventform = EventAdditionForm()
    personform  = PersonAdditionForm()
    user = {'username': 'Silas'}
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    timeline = Event.query.filter_by(incident_no=incident).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    return render_template('admin.html', title='Admin', taskf=taskform, eventf=eventform, teamf=personform,
                           user=user, tasks=tasks, impacts=impacts, inc=inc, team=team, timeline=timeline)


@app.route('/submitimpact/<incident>', methods=['GET', 'POST'])
def submitimpact(incident):
    form = ImpactStatementForm()
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()

    if form.validate_on_submit():
        sttmnt = ImpactStatement(incident_no=inc.incident_no, body=form.statement.data, submitter=form.submitter.data)

        db.session.add(sttmnt)
        db.session.commit()

        flash('Statement added: {} by {}'.format(
            form.statement.data, form.submitter.data
        ))
        return render_template('submitImpact.html', title='Submit Impact Statement for {}'.format(inc.incident_no),
                               impacts=impacts, inc=inc, impactf=form)
    else:
        return render_template('submitImpact.html', title='Submit Impact Statement for {}'.format(inc.incident_no),
                               impacts=impacts, inc=inc, impactf=form)
