from flask import Blueprint

video = Blueprint('video', __name__, template_folder='templates', static_folder='static', static_url_path='/video_static')

from . import views
