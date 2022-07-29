from flask import jsonify, request
from flask_login import current_user

from . import admin
from .scripts.login import login_required_custom, is_admin
from app.scripts.sqllite import database
from app.admin.scripts.validity_check import check_information, check_paths, check_status


@admin.route('/admin/register', methods=['POST'])
@login_required_custom
def register():
    return check_information(database.new_user)


@admin.route('/admin/user_information', methods=['POST'])
@login_required_custom
@is_admin
def user_information():
    data = request.json
    user_data = database.user_data_by_username(data['username'])
    if user_data is None:
        return jsonify(status=404, text="Username is not available"), 200
    else:
        return jsonify(status=200, id=user_data[0], paths=user_data[3],
                       services={"ftp": user_data[4], "video": user_data[5], "audio": user_data[6], "pdf": user_data[7],
                                 "receive": user_data[8], "send": user_data[9], "system_control": user_data[10],
                                 "picture": user_data[11]}), 200


@admin.route('/admin/update_access', methods=['POST'])
@login_required_custom
@is_admin
@check_paths
@check_status
def update_access():
    data = request.json
    database.update_user_information(data['username'], data['paths'], data['services']['ftp'],
                                     data['services']['video'],
                                     data['services']['audio'], data['services']['pdf'], data['services']['receive'],
                                     data['services']['send'], data['services']['system_control'],
                                     data['services']['picture'])
    return jsonify(status=200), 200
