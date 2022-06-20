from ftp.ftp_scripts.path import listdir, chdir

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS


def ftp_server(data, ip, root, perm='elr'):
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    authorizer.add_anonymous(root, perm=perm)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Instantiate AbstractedFS class
    abstracted_fs = AbstractedFS
    abstracted_fs.listdir = listdir
    abstracted_fs.chdir = chdir

    handler.abstracted_fs = abstracted_fs

    # Define a customized banner (string returned when client connects)
    handler.banner = "Welcome to HomeServer FTP "

    # Instantiate FTP server class
    address = (ip, data[5])
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 6

    return server
