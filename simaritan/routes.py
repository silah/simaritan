from simaritan import app, dashboard, modify, admin, report, auth, systems
from flask import redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    # If a user is logged in, go to overview, otherwise go to login
    return redirect(url_for('admin.overview'))


app.register_blueprint(auth.bp)

app.register_blueprint(dashboard.bp)

app.register_blueprint(modify.bp)

app.register_blueprint(admin.bp)

app.register_blueprint(report.bp)

app.register_blueprint(systems.bp)
