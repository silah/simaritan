from flask import Blueprint

bp = Blueprint('dashboard', __name__)

from simaritan.dashboard import routes