import getopt
import logging
import os
import sys
from threading import Thread
from time import sleep
from hashlib import sha256

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
from scripts.paths import add_path_database, write_paths
from ftp.ftp_scripts.filesystems import get_root
from admin.scripts.validity_check import check_username, check_password

v = 6
connected_network = False
ip = ''
LONG_OPTION = ["help", "port=", "path", "add_path=", "del_path=", "ftp_port=", "ftp_server=", "ftp_root=",
               "ftp_create_directory=", "ftp_store_file=", "login_status=", "username=", "password=", "receive_path=",
               "receive"]
OPTION = "hp:ab:d:c:e:f:g:i:j:k:l:m:n"


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


def add_path(path):
    if os.path.isdir(path):
        add_path_database(path)
        logger.info("Path added successfully")
    else:
        logger.error("The path is wrong")


def del_path(path: str) -> None:
    paths: list = database.get_data()[0].split(',')
    if path in paths:
        paths.remove(path)
        write_paths(paths)
        logger.info('The path was successfully deleted')
    else:
        logger.error('The path is not available in the program')


def save_port(port, typ):
    if check_port_bool(port):
        if typ == 'web':
            database.write_data(port, "port")
        elif typ == 'ftp':
            database.write_data(port, 'port_ftp')
        logger.info('Port changed successfully')
    else:
        logger.error('The port value must be a number')


def save_status(arg, typ):
    if arg in ['0', '1']:
        if typ == 'ftp_server':
            database.write_data(arg, 'ftp_server')
        elif typ == 'ftp_create_directory':
            database.write_data(arg, 'ftp_create_directory')
        elif typ == 'ftp_store_file':
            database.write_data(arg, 'ftp_store_file')
        elif typ == 'login_status':
            database.write_data(arg, 'login_status')
        logger.info(f'{typ} saved successfully')
    else:
        logger.error(f'The value entered for {typ} is incorrect, it should be 0 or 1')


def ftp_root_save(root):
    data = database.get_data()
    allowed_root = get_root(4, data[12])
    if root in allowed_root:
        database.write_data(root, 'ftp_root')
        logger.info('FTP Root saved successfully')
    else:
        logger.error("The entered root is wrong. You are allowed to use these roots:\n" + '\n'.join(allowed_root))


def save_username(username):
    if check_username(username):
        database.write_data(username, 'admin_username')
        logger.info('username saved successfully')
    else:
        logger.error('Enter a valid username\nusername is 4-20 characters long\nallowed characters a-z A-Z 0-9')


def save_password(password):
    if check_password(password):
        database.write_data(sha256(password.encode()).hexdigest(), 'admin_password')
        logger.info('password saved successfully')
    else:
        logger.error('Enter a valid Password\nMinimum 8 characters, at least one uppercase letter, one lowercase '
                     'letter, one number and one special character (@$!%*?&)')


def save_received_path(path):
    if os.path.isdir(path):
        database.write_data(path, "upload")
        logger.info("Received path saved successfully")
    else:
        logger.error("The path received is incorrect")


def _help():
    print('''Usage: "python manage.py runserver" to run servers
or 
python manage.py [OPTION]...
Option      Long option             Meaning
-a          --path                  Show all accessible paths of the program 
-b          --add_path              Add an accessible path, example: --add_path="/home/username/Desktop"
-c          --ftp_port              FTP port setting
-d          --del_path              Remove an access path
-e          --ftp_server            Turn off and on the FTP server, 0 or 1
-f          --ftp_root              Set FTP root
-g          --ftp_create_directory  Set FTP create directory
-h          --help                  Show this help text and exit
-i          --ftp_store_file        Set FTP store file   
-j          --login_status          Setting whether or not login is enabled, 0 or 1
-k          --username              Admin username setting
-i          --password              Admin password setting
-m          --receive_path         Setting the receiving path
-n          --receive              Show receiving path
-p          --port=<int>            Change the web app port. The port must be a number between 0 and 65535 and not already used
    ''')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, OPTION, LONG_OPTION)
    except getopt.GetoptError:
        _help()
        sys.exit(2)
    if 'runserver' in args:
        threading_start()
        sleep(2)
    else:
        for opt, arg in opts:
            match opt:
                case '-p' | '--port':
                    save_port(arg, 'web')
                case '-a' | '--path':
                    print(*database.get_data()[0].split(','), sep='\n')
                case '-b' | '--add_path':
                    add_path(arg)
                case '-c' | '--ftp_port':
                    save_port(arg, 'ftp')
                case '-d' | '--del_path':
                    del_path(arg)
                case '-e' | '--ftp_server':
                    save_status(arg, 'ftp_server')
                case '-f' | '--ftp_root':
                    ftp_root_save(arg)
                case '-g' | '--ftp_create_directory':
                    save_status(arg, 'ftp_create_directory')
                case '-h' | '--help':
                    _help()
                case '-i' | '--ftp_store_file':
                    save_status(arg, 'ftp_store_file')
                case '-j' | '--login_status':
                    save_status(arg, 'login_status')
                case '-k' | '--username':
                    save_username(arg)
                case '-l' | '--password':
                    save_password(arg)
                case '-m' | '--receive_path':
                    save_received_path(arg)
                case '-n' | '--receive':
                    print(f"received path: {database.get_data()[3]}")


if __name__ == "__main__":
    try:
        ip = get_ip()
        connected_network = True
    except OSError:
        logger.error('You are not connected to any networks')
        sys.exit(2)
    main(sys.argv[1:])
