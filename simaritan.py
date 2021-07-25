from simaritan import app, db
from models import User, Incident, ImpactStatement, Task, Event

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Incident': Incident, 'ImpactStatement': ImpactStatement, 'Task': Task, 'Event': Event}