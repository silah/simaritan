from flask import flash, url_for, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
#from werkzeug.urls import url_parse --removed as deprecated
from urllib.parse import urlparse #added in place of werkzeug
from werkzeug.utils import redirect

from models import User, Incident
from simaritan import db
from simaritan.auth import bp
from simaritan.forms import LoginForm, UserReg


@bp.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already authenticated, go to the overview page.
    if current_user.is_authenticated:
        return redirect(url_for('admin.overview'))

    # create a login form object
    form = LoginForm()

    # Condition if user is hitting Login as a result of submitting the login form
    if form.validate_on_submit():
        # Get the user data for username in question
        user = User.query.filter_by(username=form.username.data).first()
        # If data doesn't exist, or if password doesn't match, failure.
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        # if data matches, login the user.
        login_user(user, remember=form.remember_me.data)

        # Fetch the page user was trying to go to, in case login challenge was presented
        next_page = request.args.get('next')
        # Check if there is a next page arg and check that arg is for same server with netloc
        #if not next_page or url_parse(next_page).netloc != '': -- Obsolete werkzeug version
        if not next_page or urlparse(next_page).netloc != '': # new v replaceing werkzeug
            next_page = url_for('admin.overview')
        # Redirect to the next page
        return redirect(next_page)
    else:
        return render_template('pages/login.html', title='Log in to Simaritan', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/temp')
def bonga():

    user = User(username='first', name='first', email='first', role='Incident Manager', team='first')
    user.set_password('test123')

    db.session.add(user)

    db.session.commit()

    return 'Incident Management user with password: test123 created... you dumbass!!!'


@bp.route('/usermanagement', methods=['GET', 'POST'])
@login_required
def userManagement():
    # Prevent an authenticated user who is not an IM from accessing user management
    if current_user.role != "Incident Manager":
        return render_template('notpermitted.html')

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
            return render_template('pages/userManagement.html', msg='Users e-mail is already registered',
                                   users=users, regf=regf, incs=incidents, title='User Management')

        # Update the user list so showing the new user
        users = User.query.all()

        return redirect(url_for('auth.userManagement'))

    return render_template('pages/userManagement.html', users=users, regf=regf, incs=incidents, title='User Management')


@bp.route('/users/profile/<id>', methods=['GET', 'POST'])
@login_required
def userProfile(id):
    if current_user.role != "Incident Manager":
        return render_template('notpermitted.html')

    usr = User.query.get(id)
    profileform = UserReg()

    if profileform.validate_on_submit():

        if profileform.role.data == 'Please select role':
            return render_template('pages/userProfile.html', usr=usr, form=profileform, msg='Please select a role')

        usr.name = profileform.full_name.data
        usr.username = profileform.uname.data
        usr.email = profileform.email.data
        usr.role = profileform.role.data
        usr.team = profileform.team.data

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('auth.userProfile', id=usr.id, msg='Validation error. Please check all fields'))

        return redirect(url_for('auth.userManagement'))

    return render_template('pages/userProfile.html', usr=usr, form=profileform)
