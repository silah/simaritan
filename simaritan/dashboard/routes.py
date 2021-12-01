from flask import render_template

from models import Incident, ImpactStatement, Task, Event, IncMem
from simaritan.dashboard import bp

@bp.route('/dashboard')
def dashboard_blank():
    return render_template('notfound.html', incident='blank', title='Not found!')


@bp.route('/dashboard/<incident>')
def dashboard(incident):
    # Grab all the information about the incident, from the database
    inc = Incident.query.filter_by(incident_no=incident).first()

    # If there is no incident of the number accessed, send to error page
    if inc is None:
        return render_template('notfound.html', incident=incident, title='Not found!')

    # Grab all the details required for the dashboard from the database

    impacts = ImpactStatement.query.filter_by(incident_no=incident).all()
    tasks = Task.query.filter_by(incident_no=incident).all()
    # Filter the timeline by the timestamp, in descending order to get the latest times on top
    timeline = Event.query.filter_by(incident_no=incident).order_by(Event.timestamp.desc()).all()
    team = IncMem.query.filter_by(incident_no=incident).all()

    # Tally up the tasks
    total_tasks = 0
    closed_tasks = 0

    for tsk in tasks:
        total_tasks += 1
        if tsk.status == '1':
            closed_tasks += 1

    # render dashboard
    return render_template('dashboard.html', title='Incident Dashboard for {}'.format(inc.incident_no),
                           tasks=tasks, team=team, timeline=timeline, impacts=impacts, inc=inc,
                           total_tasks=total_tasks, ctasks=closed_tasks)
