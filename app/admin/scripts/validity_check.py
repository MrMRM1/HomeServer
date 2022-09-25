import re
from hashlib import sha256

from flask import request, jsonify
from flask_login import current_user

from app.scripts.sqllite import database
from app.scripts.paths import check_path
from app.admin.scripts.login import is_admin


def check_username(username: str) -> bool:
    if re.match(r'^(?=.{4,20}$)[a-zA-Z0-9]+$', username):
        return True
    else:
        return False


def check_password(password: str) -> bool:
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        return True
    else:
        return False


def check_status(function):

    def check(*args, **kwargs):
        data = request.json
        if len(data['services'].keys()) != 10:
            return jsonify(status=14, text='Services are not complete'), 200
        for i in data['services'].keys():
            if data['services'][i] == '1' or data['services'][i] == '0':
                continue
            else:
                return jsonify(status=15, text=f'The status of the {i} service is invalid', problem=i), 200
        return function(*args, **kwargs)

    check.__name__ = function.__name__
    return check


def check_paths(function):

    def check(*args, **kwargs):
        data = request.json
        path = data['paths']
        if path is not None and path != '':
            path = path.split(',')
            for i in path:
                if check_path(i) is False:
                    return jsonify(status=16, text='The path is invalid', problem=i), 200
        return function(*args, **kwargs)

    check.__name__ = function.__name__
    return check


def check_ftp_root(function):

    def check(*args, **kwargs):
        data = request.json
        path = data['ftp_root']
        if path is not None:
            roots = data['paths'].split(',')
            for i in roots:
                if path in i:
                    return function(*args, **kwargs)
        return jsonify(status=21, text='ftp_root is invalid'), 200

    check.__name__ = function.__name__
    return check


@is_admin
@check_paths
@check_status
@check_ftp_root
def check_information(func):
    data = request.json
    if check_username(data['username']) is False:
        return jsonify(status=11, text='Username is incorrect'), 200
    if data['username'] == current_user.username or database.user_data_by_username(data['username']) is not None:
        return jsonify(status=12, text='The username is already available'), 200
    if check_password(data['password']) is False:
        return jsonify(status=13, text='Password is incorrect'), 200
    if func.__name__ == 'new_user':
        func(data['username'], sha256(data['password'].encode()).hexdigest(), data['paths'],
             [data['services']['ftp'], data['services']['video'], data['services']['audio'], data['services']['pdf'],
              data['services']['receive'], data['services']['send'], data['services']['system_control'], data['services']['picture']], data['ftp_root'])
        return jsonify(status=200), 200

