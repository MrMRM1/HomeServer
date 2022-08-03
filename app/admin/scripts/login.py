import re
from functools import wraps

from flask_login import login_required, login_user, current_user
from flask import render_template, redirect, request, abort, jsonify

from app.scripts.sqllite import database
from .user import User


def login_required_custom(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if database.get_data()[11] == '1':
            try:
                secret = request.args['secret']
                secret_data = database.get_secret_data(secret)
                if secret_data and kwargs['link'] == secret_data[1]:
                    return func(*args, **kwargs)
            except KeyError:
                pass
            return login_required(func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return decorated_view


def error_login(guest_status):
    alert = 'Username or password is incorrect.'
    guest = False
    if guest_status == '1':
        guest = True
    return render_template('login.html', guest=guest, alert=alert)


def user_login(username):
    login_user(User(username))
    try:
        url = request.args['next']
        if re.findall(r'^http', url) or re.findall(r'^//', url):
            url = '/'
    except:
        url = '/'
    return redirect(url)


def access_status(location: int) -> bool:
    data = database.get_data()
    if data[11] == '1':
        username = current_user.username
        if data[12] == username:
            return True
        else:
            user_data = database.user_data_by_username(username)
            if user_data[location] == '1':
                return True
            else:
                return abort(404)
    else:
        return True


def is_admin(function):

    def check(*args, **kwargs):
        if current_user.is_admin():
            try:
                if current_user.username != request.json['username']:
                    return function(*args, **kwargs)
            except TypeError:
                return function(*args, **kwargs)
            except:
                return jsonify(status=403, text='Access is not allowed'), 200
        return jsonify(status=403, text='Access is not allowed'), 200
    check.__name__ = function.__name__
    return check
