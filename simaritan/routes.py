from simaritan import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    user = {'username': 'Silas'}
    tasks = [
        {'id': 1, 'activity': 'Feed animals', 'owner': 'Silas', 'eta': '15:00', 'status': 'Complete'},
        {'id': 2, 'activity': 'Guard Ziva', 'owner': 'Silas', 'eta': '13:40', 'status': 'Ongoing'},
        {'id': 3, 'activity': 'Eat Food', 'owner': 'Ellie', 'eta': '15:00', 'status': 'Complete'},
        {'id': 4, 'activity': 'Watch Out for food thieves', 'owner': 'Ziva', 'eta': '15:00', 'status': 'Ongoing'},
        {'id': 5, 'activity': 'Munch down chow', 'owner': 'Blackie', 'eta': '15:00', 'status': 'Complete'},
        {'id': 6, 'activity': 'Try to steal food', 'owner': 'Blackie', 'eta': '15:00', 'status': 'Ongoing'},
    ]
    details = {
        'incidentid': 'INC001276354',
        'description': 'Nigel stumbled over a bunch of cables in the Data center and a whole rack of servers fell over',
        'impact_statements': [
            {
                'submitter': 'Silas',
                'statement': 'Main website is not available'
            },
            {
                'submitter': 'Ellie the Dog',
                'statement': 'The dog food stock is running dangerously low and it may impact supply chain for items such as'
                             'tail wags, drool and dog-kisses'
            },
            {
                'submitter': 'Ziva the Cat',
                'statement': 'Meow Meow meow Meeoow Meow Maaaoooww Meow Meeoow milk milk milk!!!'
            }
        ]
    }
    team = [
        {
            'name': 'Ziva Komfykat',
            'team': 'Incident Manager'
        },
        {
            'name': 'Ellie Wag Bishop',
            'team': 'Sniffing Squad'
        },
        {
            'name': 'Blackie Milkywhisker',
            'team': 'Dairy and Produce'
        },
        {
            'name': 'Silas the Muppet',
            'team': 'Hooman servant'
        }
    ]
    return render_template('dashboard.html', title='Simaritan', user=user, tasks=tasks, details=details, team=team)
