from flask import render_template, url_for, request
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from models import Incident, ImpactStatement, Task, Event, IncMem, User
from simaritan import db
from simaritan.modify import bp


@bp.route('/update/<item>', methods=['POST'])
@login_required
def update(item):
    if item == 'deleteuser':
        # Only incident managers can do this
        if current_user.role != 'Incident Manager':
            return render_template('notpermitted.html')

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


@bp.route('/remove/<incno>/<type>/<typeid>')
@login_required
def remove_thing(incno, type, typeid):
    # Only incident managers can do this
    if current_user.role != 'Incident Manager':
        return render_template('notpermitted.html')

    # Remove the item requested

    if type == 'task':

        t = Task.query.get(typeid)
        db.session.delete(t)
        db.session.commit()

        return redirect('/admin/{}'.format(incno))

    elif type == 'event':

        e = Event.query.get(typeid)
        db.session.delete(e)
        db.session.commit()

        return redirect('/admin/{}'.format(incno))

    elif type == 'mem':

        m = IncMem.query.get(typeid)
        db.session.delete(m)
        db.session.commit()

        return redirect('/admin/{}'.format(incno))

    elif type == 'impact':

        i = ImpactStatement.query.get(typeid)
        db.session.delete(i)
        db.session.commit()

        return redirect('/admin/{}'.format(incno))

    elif type == 'inc':

        inc = Incident.query.get(typeid)
        db.session.delete(inc)
        db.session.commit()

        # Grab all the data related to the incident so it can be cleaned up
        impact_list = ImpactStatement.query.filter_by(incident_no=inc.incident_no).all()
        task_list = Task.query.filter_by(incident_no=inc.incident_no).all()
        event_list = Event.query.filter_by(incident_no=inc.incident_no).all()
        team_list = IncMem.query.filter_by(incident_no=inc.incident_no).all()

        # Delete all associated data
        for impact in impact_list:
            db.session.delete(impact)

        for tasks in task_list:
            db.session.delete(tasks)

        for events in event_list:
            db.session.delete(events)

        for members in team_list:
            db.session.delete(members)

        # Delete the incident itself
        db.session.delete(inc)

        # Commit to the database
        db.session.commit()

        return redirect(url_for('overview'))

    else:
        return render_template('notfound.html', incident=incno, title='Not found!')
