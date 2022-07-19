from app.scripts.sqllite import Database
from flask_login import login_required


def login_required_custom(func):

    def decorated_view(*args, **kwargs):
        database = Database()
        if database.get_data()[11] == '1':
            return login_required(func)(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return decorated_view