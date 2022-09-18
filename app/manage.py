import getopt
import logging
import os
import sys
from threading import Thread
from time import sleep

try:
    import sys
    sys.path.append('/'.join(os.path.dirname(sys.modules['__main__'].__file__).split('/')[:-1]))
except:
    pass

try:
    from gevent.pywsgi import WSGIServer
    gevent_import = True
except ModuleNotFoundError:
    gevent_import = False

from web_app import app
from ftp import ftp_server
from scripts.network import get_ip, check_port_bool
from scripts.sqllite import database

v = 6
connected_network = False
ip = ''


class CustomFormatter(logging.Formatter):

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    format = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: HEADER + format + ENDC,
        logging.INFO: OKCYAN + format + ENDC,
        logging.WARNING: WARNING + format + ENDC,
        logging.ERROR: FAIL + format + ENDC,
        logging.CRITICAL: BOLD + format + ENDC
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


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
    logger.info(f'Web app: http://{address_app}')
    if gevent_import:
        http_server = WSGIServer((ip, int(port_app)), app)
        http_server.serve_forever()
    else:
        logger.warning("Install gevent module for better app performance")
        app.run(host=ip, port=port_app, debug=False)


def run_ftp(data):
    """
    :return: According to the settings of the ftp server, it turns on
    """
    global address_run_ftp
    global ftp_server_control
    if data[6] == '0':
        logger.info('FTP server: disabled')
    else:
        address_run_ftp = f'Host: {ip}  Port: {data[5]}'
        if data[11] == '0':
            address_run_ftp += '  Login anonymously'
        logger.info(f'FTP server: {address_run_ftp}')
        ftp_server_control = ftp_server(data, ip)
        ftp_server_control.serve_forever(handle_exit=False)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help", "port="])
    except getopt.GetoptError:
        sys.exit(2)
    if 'runserver' in args:
        threading_start()
    else:
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                pass
            elif opt == '--port':
                if check_port_bool(arg):
                    database.write_data(arg, "port")
                    logger.info('Port changed successfully')
                else:
                    logger.error('The port value must be a number')


if __name__ == "__main__":
    try:
        ip = get_ip()
        connected_network = True
    except OSError:
        logger.error('You are not connected to any networks')
        sys.exit(2)
    main(sys.argv[1:])
    sleep(2)
