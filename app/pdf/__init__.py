from flask import Blueprint

pdf = Blueprint('pdf', __name__, template_folder='templates', static_folder='static', static_url_path='/pdf_static')

from . import views
