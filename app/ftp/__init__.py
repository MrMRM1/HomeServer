import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS

from app.ftp.ftp_scripts.filesystems import listdir, chdir, mkdir, open_fs
from app.ftp.ftp_scripts.handlers import run_as_current_user


def ftp_server(data, ip):
    """
    :param data:  database.get_data()
    :param ip:  IP system on the local network ( get_ip() )
    :return: Instantiate FTP server class
    """
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()
    perm = 'elr'
    if data[8] == '1':
        perm += 'm'
    if data[9] == '1':
        perm += 'w'
    authorizer.add_anonymous(os.path.realpath(data[7]), perm=perm)

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
