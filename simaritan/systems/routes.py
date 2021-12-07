from flask import render_template, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import redirect

from models import system
from simaritan import db
from simaritan.forms import systemAdd

from simaritan.systems import bp


@bp.route('/systems', methods=['GET', 'POST'])
@login_required
def systems_list():
    sys_add = systemAdd()
    systems = system.query.all()

    if sys_add.validate_on_submit():
        sys = system(name=sys_add.name.data, category=sys_add.category.data, owner=sys_add.owner.data,
                     primary_contact=sys_add.primary_contact.data, contact_number=sys_add.contact_number.data,
                     contact_email=sys_add.contact_email.data, priority=sys_add.priority.data)

        # Add to DB
        db.session.add(sys)
        # Try to commit and catch exception where the Users email is already registered
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('systems.system_list'))

    return render_template('pages/systemsList.html', systems=systems, sys_add=sys_add)


@bp.route('/systems/profile/<id>', methods=['GET', 'POST'])
@login_required
def systemProfile(id):

    sys = system.query.get(id)
    sysform = systemAdd()

    if sysform.validate_on_submit():

        sys.name = sysform.name.data
        sys.category = sysform.category.data
        sys.owner = sysform.owner.data
        sys.primary_contact = sysform.primary_contact.data
        sys.contact_number = sysform.contact_number.data
        sys.contact_email = sysform.contact_email.data
        sys.priority = sysform.priority.data

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('systems.systemProfile', id=sys.id, msg='Validation error. Please check all fields'))

        return redirect(url_for('systems.systems_list'))

    return render_template('pages/systemProfile.html', sys=sys, form=sysform)
