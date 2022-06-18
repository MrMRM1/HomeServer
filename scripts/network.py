import os
from socket import socket, AF_INET, SOCK_DGRAM


def port_flask():
    if os.name == 'nt':
        return 80
    else:
        return 8880


def get_ip():
    """
    :return: local ip
    """
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
