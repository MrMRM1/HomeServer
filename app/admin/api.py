from . import admin
from .scripts.login import login_required_custom
from app.scripts.sqllite import database
from app.admin.scripts.validity_check import check_information


@admin.route('/admin/register', methods=['POST'])
@login_required_custom
def register():
    return check_information(database.new_user)
