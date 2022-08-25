from flask import Blueprint

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static', static_url_path='/admin_static')

from . import api
from . import views
