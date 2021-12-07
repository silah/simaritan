from flask import render_template, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from models import Incident, ImpactStatement, Task, Event, IncMem
from simaritan import db
from simaritan.admin import bp
from simaritan.forms import TaskAdditionForm, EventAdditionForm, PersonAdditionForm, ImpactStatementForm, IncidentStart


@bp.route('/admin')
@login_required
def admin_blank():
    return render_template('notfound.html', incident='blank', title='Not found!')


@bp.route('/admin/<incident>', methods=['GET', 'POST'])
@login_required
def admin(incident):
    # Prevent an authenticated user who is not an IM from editing an incident
    if current_user.role != "Incident Manager":
        return render_template('notpermitted.html')

    # Create the Form objects
    taskform = TaskAdditionForm()
    eventform = EventAdditionForm()
    personform = PersonAdditionForm()
    impactf = ImpactStatementForm()

    inc = Incident.query.filter_by(incident_no=incident).first()

    # If non-existing incident is accessed, show the not found page.
    if inc is None:
        return render_template('notfound.html', incident=incident, title='Not found!')

    # Fetch all the information about the incident.
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    # tally up the tasks
    total_tasks = 0
    closed_tasks = 0

    for tsk in tasks:
        total_tasks += 1
        if tsk.status == '1':
            closed_tasks += 1

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
        return render_template('pages/dashboardContent.html', title='Admin Section for {}'.format(inc.incident_no),
                               taskf=taskform,
                               eventf=eventform, teamf=personform, tasks=tasks, impacts=impacts, inc=inc,
                               team=team, timeline=timeline, admin=True, total_tasks=total_tasks, ctasks=closed_tasks,
                               impactf=impactf)


@bp.route('/admin/close/<incident>')
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

        return redirect(url_for('admin.overview'))
    else:
        return render_template('notpermitted.html')

@bp.route('/submitimpact/<incident>', methods=['GET', 'POST'])
def submitimpact(incident):
    form = ImpactStatementForm()
    inc = Incident.query.filter_by(incident_no=incident).first()
    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()

    # Get tasks for the header counter
    tasks = Task.query.filter_by(incident_no=inc.incident_no).all()

    # Tally up the tasks
    total_tasks = 0
    closed_tasks = 0

    for tsk in tasks:
        total_tasks += 1
        if tsk.status == '1':
            closed_tasks += 1

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
        return redirect('/admin/{}'.format(incident))
    else:
        return redirect('/admin/{}'.format(incident))


@bp.route('/overview', methods=['GET', 'POST'])
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

    return render_template('pages/incidentOverview.html', incf=incf, incs=users_incidents, title='Managers overview')
