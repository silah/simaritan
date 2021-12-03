from flask import flash, url_for, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.urls import url_parse
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
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.overview')
        # Redirect to the next page
        return redirect(next_page)
    else:
        return render_template('pages/login.html', title='Log in to Simaritan', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


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
            return render_template('/userManagement.html', msg='Users e-mail is already registered',
                                   users=users, regf=regf, incs=incidents, title='User Management')

        # Update the user list so showing the new user
        users = User.query.all()

        return redirect(url_for('auth.userManagement'))

    return render_template('pages/userManagement.html', users=users, regf=regf, incs=incidents, title='User Management')


@bp.route('/users/profile', methods=['GET', 'POST'])
@login_required
def userProfile():

    return render_template('pages/userProfile.html')