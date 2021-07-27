from simaritan import app
from flask import render_template, flash, redirect
from simaritan.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    loggedin = False
    if loggedin:
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect('/index')
    else:
        return render_template('login.html', title='Log in', form=form)


@app.route('/dashboard')
def dashboard():
    user = {'username': 'Silas'}
    tasks = [
        {'id': 1, 'activity': 'Send Business Comms', 'owner': 'Silas', 'eta': '15:30', 'status': 'Complete'},
        {'id': 2, 'activity': 'Untangle Cables', 'owner': 'Ziva', 'eta': '13:40', 'status': 'Ongoing'},
        {'id': 3, 'activity': 'Plug cables back in', 'owner': 'Ziva', 'eta': '15:30', 'status': 'Ongoing'},
        {'id': 5, 'activity': 'Gather Impact Statements', 'owner': 'Simon', 'eta': '15:00', 'status': 'Complete'},
        {'id': 6, 'activity': 'Inform business owners', 'owner': 'Silas', 'eta': '15:00', 'status': 'Ongoing'},
    ]
    timeline = [
        {'id': 1, 'activity': 'Task completed: "Untangle cables"', 'owner': 'Ziva the Cat', 'eta': '15:15', 'type': 'Task completed'},
        {'id': 2, 'activity': 'Server Team joined call', 'owner': 'Ellie', 'eta': '15:10', 'type':'Call update'},
        {'id': 3, 'activity': 'Call centre impact added', 'owner': 'Simon', 'eta': '15:00', 'type': 'Impact clarification'},
        {'id': 4, 'activity': 'Business Stakeholder joined call', 'owner': 'Simon', 'eta': '15:00', 'type':'Call update'},
        {'id': 5, 'activity': 'Incident bridge initiated: Conference code 1234', 'owner': 'Silas', 'eta': '14:45', 'type':'Call update'},
        {'id': 6, 'activity': 'Incident Started', 'owner': 'Silas', 'eta': '14:34', 'type':'Call update'}

    ]
    details = {
        'incidentid': 'INC001276354',
        'description': 'Nigel stumbled over a bunch of cables in the Data center and a whole rack of servers fell over',
        'impact_statements': [
            {
                'submitter': 'Silas - Incident Management Muppet',
                'statement': 'Main website is not available'
            },
            {
                'submitter': 'Simon the Business Stakeholder',
                'statement': 'Call centre is getting calls from customers saying they cannot log into shopping basket'
            },
            {
                'submitter': 'Ziva the Cat',
                'statement': 'Meow Meow meow Meeoow Meow Maaaoooww Meow Meeoow milk milk milk!!!'
            }
        ]
    }
    team = [
        {
            'name': 'Silas Wulff Hansen',
            'team': 'Incident Manager'
        },
        {
            'name': 'Ellie Bishop',
            'team': 'Sniffing Squad'
        },
        {
            'name': 'John Silver',
            'team': 'The Pirate Crew'
        },
        {
            'name': 'Simon Longbottom',
            'team': 'Customer Call Centre'
        }
    ]
    return render_template('dashboard.html', title='Simaritan', user=user, tasks=tasks, details=details, team=team, timeline=timeline)
