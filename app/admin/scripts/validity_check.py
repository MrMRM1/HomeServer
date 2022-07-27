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


def check_information(func):
    username_admin = database.get_data()[12]
    if current_user.username == username_admin:
        data = request.json
        if check_username(data['username']) is False:
            return jsonify(status=11, test='Username is incorrect'), 200
        if data['username'] == username_admin or database.get_user_data(data['username']) is not None:
            return jsonify(status=12, test='The username is already available'), 200
        if check_password(data['password']) is False:
            return jsonify(status=13, test='Password is incorrect'), 200
        if len(data['services'].keys()) != 8:
            return jsonify(status=14, test='Services are not complete'), 200
        for i in data['services'].keys():
            if data['services'][i] == '1' or data['services'][i] == '0':
                continue
            else:
                return jsonify(status=15, test=f'The status of the {i} service is invalid', service=i), 200
        path = data['paths']
        if path is not None:
            path = path.split(',')
            for i in path:
                if check_path(i) is False:
                    return jsonify(status=16, test='The path is invalid', service=i), 200
            path = ','.join(path)
        if func.__name__ == 'new_user':
            func(data['username'], sha256(data['password'].encode()).hexdigest(), path,
                 [data['services']['ftp'], data['services']['video'], data['services']['audio'], data['services']['pdf'],
                  data['services']['receive'], data['services']['send'], data['services']['system_control'], data['services']['picture']])
            return jsonify(status=200), 200

    return jsonify(status=403, text='Access is not allowed'), 200
