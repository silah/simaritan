from flask_login import login_user, current_user, logout_user, login_required

from werkzeug.urls import url_parse

from simaritan import app, db
from flask import render_template, flash, redirect, url_for, request, make_response
from simaritan.forms import LoginForm, TaskAdditionForm, EventAdditionForm, PersonAdditionForm, ImpactStatementForm, \
    IncidentStart, UserReg
from models import Incident, IncMem, ImpactStatement, Task, Event, User
from sqlalchemy.exc import IntegrityError


@app.route('/')
@app.route('/index')
def index():
    # If a user is logged in, go to overview, otherwise go to login
    return redirect(url_for('overview'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already authenticated, go to the overview page.
    if current_user.is_authenticated:
        return redirect(url_for('overview'))

    # create a login form object
    form = LoginForm()

    # Condition if user is hitting Login as a result of submitting the login form
    if form.validate_on_submit():
        # Get the user data for username in question
        user = User.query.filter_by(username=form.username.data).first()
        # If data doesn't exist, or if password doesn't match, failure.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        # if data matches, login the user.
        login_user(user, remember=form.remember_me.data)

        # Fetch the page user was trying to go to, in case login challenge was presented
        next_page = request.args.get('next')
        # Check if there is a next page arg and check that arg is for same server with netloc
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('overview')
        # Redirect to the next page
        return redirect(next_page)
    else:
        return render_template('login.html', title='Log in to Simaritan', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/usermanagement', methods=['GET', 'POST'])
@login_required
def userManagement():
    users = User.query.all()
    regf = UserReg()
    incidents = Incident.query.order_by(Incident.id.asc()).all()

    if regf.validate_on_submit():
        # Grab details from Form and create a User object
        usr = User(username=regf.uname.data, name=regf.full_name.data, email=regf.email.data, role=regf.role.data,
                   team=regf.team.data)
        # Set users password
        usr.set_password(regf.password.data)

        # Add to DB
        db.session.add(usr)
        # Try to commit and catch exception where the Users email is already registered
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('/userManagement.html', msg='Users e-mail is already registered',
                                   users=users, regf=regf, incs=incidents, title='User Management')

        # Update the user list so showing the new user
        users = User.query.all()

        return redirect(url_for('userManagement'))

    return render_template('userManagement.html', users=users, regf=regf, incs=incidents, title='User Management')


@app.route('/overview', methods=['GET', 'POST'])
@login_required
def overview():
    # Create an Instatiation form object
    incf = IncidentStart()
    # Get the incidents for the logged in user, so they can be displayed
    users_incidents = Incident.query.order_by(Incident.id.asc()).all()

    # If the incident form is submitted
    if incf.validate_on_submit():
        # Create an incident
        incident = Incident(incident_no=incf.inc_no.data, description=incf.description.data,
                            status='open', inc_mgr=current_user.id)
        # Create a timeline event for the incident, denominating the start
        event = Event(body='Incident Opened: {}'.format(incf.inc_no.data), assignee=current_user.username,
                      activity='Incident Started', incident_no=incf.inc_no.data)
        # Set the incident manager
        incmem = IncMem(incident_no=incf.inc_no.data, person=incf.inc_mgr.data, role='Incident Manager')
        # Write to database
        db.session.add(incident)
        db.session.add(event)
        db.session.add(incmem)
        db.session.commit()
        # Go to admin for the incident
        return redirect('/admin/{}'.format(incf.inc_no.data))

    return render_template('overview.html', incf=incf, incs=users_incidents, title='Managers overview')


@app.route('/dashboard/<incident>')
def dashboard(incident):

    # Grab all the information about the incident, from the database
    inc = Incident.query.filter_by(incident_no=incident).first()

    # If there is no incident of the number accessed, send to error page
    if inc is None:
        return render_template('notfound.html', incident=incident, title='Not found!')

    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    # Filter the timeline by the timestamp, in descending order to get the latest times on top
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    team = IncMem.query.filter_by(incident_no=incident).all()
    # render dashboard
    return render_template('dashboard.html', title='Incident Dashboard for {}'.format(inc.incident_no),
                           tasks=tasks, team=team, timeline=timeline, impacts=impacts, inc=inc)


# Handle access to dashboard and admin route, with no incident no provided
@app.route('/dashboard')
def dashboard_blank():
    return render_template('notfound.html', incident='blank', title='Not found!')


@app.route('/admin')
@login_required
def admin_blank():
    return render_template('notfound.html', incident='blank', title='Not found!')


@app.route('/admin/<incident>', methods=['GET', 'POST'])
@login_required
def admin(incident):
    # Create the Form objects
    taskform = TaskAdditionForm()
    eventform = EventAdditionForm()
    personform = PersonAdditionForm()

    inc = Incident.query.filter_by(incident_no=incident).first()

    # If non-existing incident is accessed, show the not found page.
    if inc is None:
        return render_template('notfound.html', incident=incident, title='Not found!')

    # Fetch all the information about the incident.
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

        return redirect('/admin/{}'.format(incident))

    elif eventform.validate_on_submit():

        event = Event(body=eventform.event.data, assignee=eventform.owner.data, activity=eventform.activity_type.data,
                      incident_no=inc.incident_no)

        db.session.add(event)
        db.session.commit()

        return redirect('/admin/{}'.format(incident))

    elif personform.validate_on_submit():
        prson = IncMem(incident_no=inc.incident_no, person=personform.person.data, role=personform.role.data)
        event = Event(body='{}, {} - Joined the incident team'.format(personform.person.data, personform.role.data),
                      assignee=personform.role.data, activity='Person joined',
                      incident_no=inc.incident_no)
        db.session.add(prson)
        db.session.add(event)
        db.session.commit()

        return redirect('/admin/{}'.format(incident))

    else:
        return render_template('admin.html', title='Admin Section for {}'.format(inc.incident_no), taskf=taskform,
                               eventf=eventform, teamf=personform, tasks=tasks, impacts=impacts, inc=inc,
                               team=team, timeline=timeline)


@app.route('/admin/close/<incident>')
@login_required
def closeinc(incident):

    if incident is None:
        return render_template('notfound.html', incident=incident, title='Not found!')

    if current_user.role == "Incident Manager":
        inc = Incident.query.filter_by(incident_no=incident).first()
        inc.status = 'closed'
        event = Event(body='Incident {} has been closed by {}'.format(incident, current_user.username),
                      assignee=current_user.username, activity='Incident Closure',
                      incident_no=incident)

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('overview'))
    else:
        return render_template('notpermitted.html')


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


@app.route('/report/<incident>')
@login_required
def report(incident):
    # Get the timeline for the CSV file
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    # Start with a blank string
    csv = 'Time,Submitter,Activity,Description'
    for t in timeline:
        csv += '\n{},{},{},{}'.format(t.timestamp, t.assignee, t.activity, t.body)

    response = make_response(csv)
    cd = 'attachment; filename=report_{}'.format(incident)
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response


@app.route('/update/<item>', methods=['POST'])
@login_required
def update(item):
    if item == 'deleteuser':
        # grab form data
        usrid = request.form.get("userid")
        # execute database action
        usr = User.query.get(usrid)
        db.session.delete(usr)
        db.session.commit()

        return redirect(url_for('userManagement'))
    elif item == 'completetask':
        # grab form data
        taskid = request.form.get("taskid")
        incno = request.form.get("inc")

        # Alter the task
        tsk = Task.query.get(taskid)
        tsk.status = '1'

        # Create a timeline event for the action
        event = Event(body='Task Completed: {}'.format(tsk.body), assignee=tsk.assignee, activity='Task Completed',
                      incident_no=incno)
        # Add and commit
        db.session.add(event)

        db.session.commit()

        return redirect('/dashboard/{}'.format(incno))
    else:
        return redirect(url_for('overview'))
