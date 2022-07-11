from flask import Blueprint

picture = Blueprint('picture', __name__, template_folder='templates', static_folder='static', static_url_path='/picture_static')

from . import views
