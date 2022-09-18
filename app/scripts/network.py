import os
from socket import socket, AF_INET, SOCK_DGRAM


def port_flask() -> str:
    if os.name == 'nt':
        return '80'
    else:
        return '8880'


def get_ip() -> str:
    """
    :return: local ip
    """
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def check_port_bool(port: str) -> bool:
    try:
        port_number = str(int(port))
        if len(port) == len(port_number) and port != '':
            return True
        else:
            return False
    except ValueError:
        return False
