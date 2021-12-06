from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager

from config import Config
import pymysql
pymysql.install_as_MySQLdb()

# Naming conventions are added to get around SQLite database limitation around altering tables.
# They are passed into the DB initialization
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = Flask(__name__)
app.config.from_object(Config)
# Define the Database, adding Metadata to get around the SQLite limitation around altering databases
db = SQLAlchemy(app=app, metadata=MetaData(naming_convention=naming_convention))
# db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'auth.login'

from simaritan import routes
import models

