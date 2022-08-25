from flask import render_template, abort
from flask_login import current_user

from . import admin
from app.admin.scripts.login import login_required_custom


@admin.route('/admin')
@login_required_custom
def admin_page():
    if current_user.is_admin():
        return render_template("dashboard.html")
    else:
        return abort(404)
