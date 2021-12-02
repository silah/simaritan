from flask import render_template, url_for
from flask_login import login_required
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
                     contact_email=sys_add.contact_email.data,)

        # Add to DB
        db.session.add(sys)
        # Try to commit and catch exception where the Users email is already registered
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('systems.system_list'))

    return render_template('pages/systemsList.html', systems=systems, sys_add=sys_add)
