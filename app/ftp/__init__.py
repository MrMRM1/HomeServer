import os

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS

from app.ftp.ftp_scripts.filesystems import listdir, chdir, mkdir, open_fs
from app.ftp.ftp_scripts.handlers import run_as_current_user
from app.ftp.ftp_scripts.authorizers import DummySha256Authorizer
from app.scripts.sqllite import database


def perm_generate(create, store):
    perm = 'elr'
    if create == '1':
        perm += 'm'
    if store == '1':
        perm += 'w'
    return perm


def check_login(data, authorizer):

    if data[11] == '1':

        authorizer.add_user(data[12], data[13], os.path.realpath(data[7]), perm_generate(data[8], data[9]))
        all_users = database.ftp_users()
        try:
            start = 0
            if all_users[0][0] == 'guest':
                start = 1
                if data[14] == '1':
                    authorizer.add_anonymous(homedir=os.path.realpath(all_users[0][2]),
                                             perm=perm_generate(all_users[0][3], all_users[0][4]))

            for i in all_users[start:]:
                authorizer.add_user(i[0], i[1], os.path.realpath(i[2]), perm=perm_generate(i[3], i[4]))
        except IndexError:
            pass
    else:
        authorizer.add_anonymous(os.path.realpath(data[7]), perm=perm_generate(data[8], data[9]))


def ftp_server(data, ip):
    """
    :param data:  database.get_data()
    :param ip:  IP system on the local network ( get_ip() )
    :return: Instantiate FTP server class
    """
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummySha256Authorizer()

    check_login(data, authorizer)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Instantiate AbstractedFS class
    abstracted_fs = AbstractedFS
    abstracted_fs.listdir = listdir
    abstracted_fs.chdir = chdir
    abstracted_fs.mkdir = mkdir
    abstracted_fs.open = open_fs

    handler.abstracted_fs = abstracted_fs
    handler.run_as_current_user = run_as_current_user

    # Define a customized banner (string returned when client connects)
    handler.banner = "Welcome to HomeServer FTP "

    # Instantiate FTP server class
    address = (ip, data[5])
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 6

    return server
