from threading import Thread

try:
    from gevent.pywsgi import WSGIServer
    gevent_import = True
except ModuleNotFoundError:
    gevent_import = False

from web_app import app
from ftp import ftp_server
from scripts.network import get_ip
from scripts.sqllite import database


ip = get_ip()


def threading_start(web, ftp):
    """
    :return: Function to execute the flask program in the form of threading
    """
    global run_app
    global ftp_app
    data = database.get_data()
    run_app = Thread(target=run, args=(data[1], web,))
    run_app.start()
    ftp_app = Thread(target=run_ftp, args=(data, ftp,))
    ftp_app.start()


def run(port_app, func):
    """
    :param port_app: Port for the program to run
    :return: Disable different sections of the main window and run the flask program
    """
    global address_run
    global http_server

    func(port_app)
    if gevent_import:
        http_server = WSGIServer((ip, int(port_app)), app)
        http_server.serve_forever()
    else:
        app.run(host=ip, port=port_app, debug=False)


def run_ftp(data, func):
    """
    :return: According to the settings of the ftp server, it turns on
    """
    global address_run_ftp
    global ftp_server_control
    func(data)
    if data[6] != '0':
        ftp_server_control = ftp_server(data, ip)
        ftp_server_control.serve_forever(handle_exit=False)

    return True
