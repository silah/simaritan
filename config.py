import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1234'
    # Path to the SQLite Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Do we want notifications everytime a change is made to DB ?
    SQLALCHEMY_TRACK_MODIFICATIONS = False
