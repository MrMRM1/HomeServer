from hashlib import sha256

from flask import jsonify, request
from flask_login import current_user

from . import admin
from .scripts.login import login_required_custom, is_admin
from app.scripts.sqllite import database
from app.admin.scripts.validity_check import check_information, check_paths, check_status, check_username, check_password, check_ftp_root
from app.ftp.ftp_scripts.filesystems import get_root
from app.scripts.network import check_port_bool


@admin.route('/admin/register', methods=['POST'])
@login_required_custom
@is_admin
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
                                 "picture": user_data[11], "ftp_create_directory": user_data[12],
                                 "ftp_store_file": user_data[13]}, ftp_root=user_data[14]), 200


@admin.route('/admin/update_access', methods=['POST'])
@login_required_custom
@is_admin
@check_paths
@check_status
@check_ftp_root
def update_access():
    data = request.json
    database.update_user_information(data['username'], data['paths'], data['services']['ftp'],
                                     data['services']['video'],
                                     data['services']['audio'], data['services']['pdf'], data['services']['receive'],
                                     data['services']['send'], data['services']['system_control'],
                                     data['services']['picture'], data['services']['ftp_create_directory'],
                                     data['services']['ftp_store_file'], data['ftp_root'])
    return jsonify(status=200), 200


@admin.route('/admin/update_username', methods=['POST'])
@login_required_custom
@is_admin
def update_username():
    data = request.json
    if check_username(data['username']) is False:
        return jsonify(status=11, text='Username is incorrect'), 200
    if database.user_data_by_username(data['username']) is not None:
        return jsonify(status=12, text='The username is already available'), 200
    if data['id'] == 1 or data['id'] == '1':
        return jsonify(status=20, text='guest username cannot be changed'), 200
    database.write_users_data(data['username'], 'username', data['id'])
    return jsonify(status=200), 200


@admin.route('/admin/update_password', methods=['POST'])
@login_required_custom
@is_admin
def update_password():
    data = request.json
    user_data = database.user_data_by_username(data['username'])
    if user_data is None:
        return jsonify(status=17, text='Username is not available'), 200
    if check_password(data['password']) is False:
        return jsonify(status=13, text='Password is incorrect'), 200
    if data['password'] != data['password_verification']:
        return jsonify(status=18, text='The password must match the verification password'), 200
    if data['username'] == 'guest':
        return jsonify(status=19, text='cannot set password for guest'), 200
    database.write_users_data(sha256(data['password'].encode()).hexdigest(), 'password', user_data[0])
    return jsonify(status=200), 200


@admin.route('/admin/get_ftp_root', methods=['POST'])
@login_required_custom
@is_admin
def get_ftp_root():
    data = request.json
    user_data = database.user_data_by_username(data['username'])
    if user_data is None:
        return jsonify(status=17, text='Username is not available'), 200
    return jsonify(status=200, roots=get_root(data['advance'], data['username'])), 200


@admin.route('/admin/information_all_users', methods=['POST'])
@login_required_custom
@is_admin
def information_all_users():
    return jsonify(status=200, users=database.information_all_users()), 200


@admin.route('/admin/get_all_users', methods=['POST'])
@login_required_custom
@is_admin
def get_all_users():
    return jsonify(status=200, users=database.get_all_users()), 200


@admin.route('/admin/get_paths', methods=['POST'])
@login_required_custom
@is_admin
def get_paths():
    return jsonify(status=200, paths=database.get_data()[0]), 200


@admin.route('/admin/system_control_password', methods=['POST'])
@login_required_custom
@is_admin
def system_control_password():
    data = request.json
    if check_password(data['password']) is False:
        return jsonify(status=13, text='Password is incorrect'), 200
    if data['password'] != data['password_verification']:
        return jsonify(status=18, text='The password must match the verification password'), 200
    database.write_data(sha256(data['password'].encode()).hexdigest(), "password")
    return jsonify(status=200), 200


@admin.route('/admin/set_mode', methods=['POST'])
@login_required_custom
@is_admin
def set_mode():
    data = request.json
    status = data['status']
    if status in ['0', '1']:
        match data['mode']:
            case 'guest':
                database.write_data(status, 'guest_status')
                return jsonify(status=200), 200
            case 'login':
                database.write_data(status, 'login_status')
                return jsonify(status=200), 200
            case 'ftp':
                database.write_data(status, 'ftp_server')
                return jsonify(status=200), 200
            case 'ftp_create_directory':
                database.write_data(status, 'ftp_create_directory')
                return jsonify(status=200), 200
            case 'ftp_store_file':
                database.write_data(status, 'ftp_store_file')
                return jsonify(status=200), 200
            case 'run_background':
                database.write_data(status, 'run_background')
                return jsonify(status=200), 200
            case _:
                return jsonify(status=23, text=f'There is no {data["mode"]} mode')
    return jsonify(status=22, text=f'{data["mode"]} mode must be 0 or 1'), 200


@admin.route('/admin/set_port', methods=['POST'])
@login_required_custom
@is_admin
def set_port():
    data = request.json
    port = data['port']
    if check_port_bool(port):
        match data['type']:
            case 'web':
                database.write_data(port, "port")
            case 'ftp':
                database.write_data(port, 'port_ftp')
            case _:
                return jsonify(status=24, text="The port value must be a number"), 200
        return jsonify(status=200), 200
    else:
        return jsonify(status=25, text="Only able to change web or ftp port"), 200
