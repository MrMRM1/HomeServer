from ftp.scripts.path import listdir

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS


# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

authorizer.add_anonymous('.', perm='elr')

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Instantiate AbstractedFS class
abstracted_fs = AbstractedFS
abstracted_fs.listdir = listdir

handler.abstracted_fs = abstracted_fs

# Define a customized banner (string returned when client connects)
handler.banner = "pyftpdlib based ftpd ready."

# Instantiate FTP server class and listen on 0.0.0.0:2121
address = ('', 2121)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 6

# start ftp server
server.serve_forever(handle_exit=False)
