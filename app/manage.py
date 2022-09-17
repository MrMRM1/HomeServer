import sys
import os
from threading import Thread
from time import sleep
import logging
try:
    import sys
    sys.path.append('/'.join(os.path.dirname(sys.modules['__main__'].__file__).split('/')[:-1]))
except:
    pass

from gevent.pywsgi import WSGIServer

from web_app import app
from ftp import ftp_server
from scripts.network import get_ip
from scripts.sqllite import database

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
v = 6
connected_network = False
ip = ''


def threading_start():
    """
    :return: Function to execute the flask program in the form of threading
    """
    global run_app
    global ftp_app
    data = database.get_data()
    run_app = Thread(target=run, args=(data[1],))
    run_app.start()
    ftp_app = Thread(target=run_ftp, args=(data,))
    ftp_app.start()


def run(port_app):
    """
    :param port_app: Port for the program to run
    :return: Disable different sections of the main window and run the flask program
    """
    global address_run
    global http_server
    if port_app == '80':
        address_app = str(ip)
    else:
        address_app = f"{ip}:{port_app}"
    logging.info(f'Web app: http://{address_app}')
    database.write_data(port_app, "port")
    http_server = WSGIServer((ip, int(port_app)), app)
    http_server.serve_forever()


def run_ftp(data):
    """
    :return: According to the settings of the ftp server, it turns on
    """
    global address_run_ftp
    global ftp_server_control
    if data[6] == '0':
        logging.info('FTP server: disabled')
    else:
        address_run_ftp = f'Host: {ip}  Port: {data[5]}'
        if data[11] == '0':
            address_run_ftp += '  Login anonymously'
        logging.info(f'FTP server: {address_run_ftp}')
        ftp_server_control = ftp_server(data, ip)
        ftp_server_control.serve_forever(handle_exit=False)


def main(argv):
    if 'runserver' in argv:
        threading_start()


if __name__ == "__main__":
    try:
        ip = get_ip()
        connected_network = True
    except OSError:
        logging.error('You are not connected to any networks')
        exit()
    main(sys.argv[1:])
    sleep(2)
