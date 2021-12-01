from flask import Blueprint

bp = Blueprint('auth', __name__)

from simaritan.auth import routes