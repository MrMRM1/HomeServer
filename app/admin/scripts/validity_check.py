import re


def username_check(username: str) -> bool:
    if re.match(r'^(?=.{6,20}$)[a-zA-Z0-9]+$', username):
        return True
    else:
        return False


def password_check(password: str) -> bool:
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        return True
    else:
        return False
