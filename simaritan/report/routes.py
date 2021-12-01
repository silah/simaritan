from flask import make_response, render_template
from flask_login import login_required, current_user

from models import Event, Task
from simaritan.report import bp


@bp.route('/report/event/<incident>')
@login_required
def report_event(incident):
    # All authenticated users can do this

    # Get the timeline for the CSV file
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    # Start with a blank string
    csv = 'Time,Submitter,Activity,Description'
    for t in timeline:
        csv += '\n{},{},{},{}'.format(t.timestamp, t.assignee, t.activity, t.body)

    response = make_response(csv)
    cd = 'attachment; filename=event_report_{}'.format(incident)
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response


@bp.route('/report/tasks/<incident>')
@login_required
def report_task(incident):
    # All authenticated users can do this
    # Only incident managers can do this
    if current_user.role != 'Incident Manager':
        return render_template('notpermitted.html')

    # Get the tasks for the CSV file
    tasks = Task.query.filter_by(incident_no=incident).all()
    # Start with a blank string
    csv = 'ETA,Assignee,Description'
    for t in tasks:
        # If task is open, add to CSV
        if t.status == "0":
            csv += '\n{},{},{}'.format(t.eta, t.assignee, t.body)

    response = make_response(csv)
    cd = 'attachment; filename=open_tasks_{}'.format(incident)
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response