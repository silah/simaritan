from flask import Blueprint

bp = Blueprint('systems', __name__)

from simaritan.systems import routes