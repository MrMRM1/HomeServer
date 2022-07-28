import re
from hashlib import sha256

from flask import request, jsonify
from flask_login import current_user

from app.scripts.sqllite import database
from app.scripts.paths import check_path


def check_username(username: str) -> bool:
    if re.match(r'^(?=.{6,20}$)[a-zA-Z0-9]+$', username):
        return True
    else:
        return False


def check_password(password: str) -> bool:
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        return True
    else:
        return False


def check_status(data):
    for i in data['services'].keys():
        if data['services'][i] == '1' or data['services'][i] == '0':
            continue
        else:
            return [i]
    return True


def check_paths(data):
    path = data['paths']
    if path is not None:
        path = path.split(',')
        for i in path:
            if check_path(i) is False:
                return [i]
        path = ','.join(path)
    return path


def check_information(func):
    username_admin = database.get_data()[12]
    if current_user.username == username_admin:
        data = request.json
        if check_username(data['username']) is False:
            return jsonify(status=11, text='Username is incorrect'), 200
        if data['username'] == username_admin or database.user_data_by_username(data['username']) is not None:
            return jsonify(status=12, text='The username is already available'), 200
        if check_password(data['password']) is False:
            return jsonify(status=13, text='Password is incorrect'), 200
        if len(data['services'].keys()) != 8:
            return jsonify(status=14, text='Services are not complete'), 200
        status = check_status(data)
        if isinstance(status, list):
            return jsonify(status=15, text=f'The status of the {status[0]} service is invalid', problem=status[0]), 200
        path = check_paths(data)
        if isinstance(path, list):
            return jsonify(status=16, text='The path is invalid', problem=path[0]), 200
        if func.__name__ == 'new_user':
            func(data['username'], sha256(data['password'].encode()).hexdigest(), path,
                 [data['services']['ftp'], data['services']['video'], data['services']['audio'], data['services']['pdf'],
                  data['services']['receive'], data['services']['send'], data['services']['system_control'], data['services']['picture']])
            return jsonify(status=200), 200

    return jsonify(status=403, text='Access is not allowed'), 200
