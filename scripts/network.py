import os


def port_flask():
    if os.name == 'nt':
        return 80
    else:
        return 8880
