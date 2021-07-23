from flask import Blueprint

admin_bp = Blueprint('admnin', __name__, template_folder='templates')

from . import vistas