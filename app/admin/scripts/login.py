from functools import wraps

from flask_login import login_required

from app.scripts.sqllite import database


def login_required_custom(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if database.get_data()[11] == '1':
            return login_required(func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return decorated_view
