from flask import Blueprint

bp = Blueprint('modify', __name__)

from simaritan.modify import routes