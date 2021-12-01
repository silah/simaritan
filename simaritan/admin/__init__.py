from flask import Blueprint

bp = Blueprint('admin', __name__)

from simaritan.admin import routes