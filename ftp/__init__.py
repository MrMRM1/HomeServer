import os
from scripts.paths import check_dir_ftp, list_dir

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS


def listdir(self, root):
    allowed = list_dir()
    list_dir_allowed = []
    list_dir_root = os.listdir(root)
    for i in list_dir_root:
        path = os.path.join(root, i).replace('\\', '/')
        for j in allowed:
            if path in j:
                list_dir_allowed.append(i)
                break
            else:
                if os.path.isfile(path):
                    if root.replace('\\', '/') == j:
                        list_dir_allowed.append(i)
                        break
    return list_dir_allowed


# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions and a read-only
# anonymous user
authorizer.add_user('user', '12345', 'I:\\', perm='elr')
authorizer.add_anonymous(os.getcwd())


# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer
abstracted_fs = AbstractedFS
abstracted_fs.listdir = listdir


handler.abstracted_fs = abstracted_fs

# handler.ftp_LIST = ftp_LIST.__get__(handler, FTPHandler)
# handler.ftp_NLST = ftp_NLST.__get__(handler, FTPHandler)
# handler.ftp_MLSD= ftp_MLSD

# Define a customized banner (string returned when client connects)
handler.banner = "pyftpdlib based ftpd ready."

# Specify a masquerade address and the range of ports to use for
# passive connections.  Decomment in case you're behind a NAT.
#handler.masquerade_address = '151.25.42.11'
#handler.passive_ports = range(60000, 65535)

# Instantiate FTP server class and listen on 0.0.0.0:2121
address = ('192.168.1.101', 2121)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# start ftp server
server.serve_forever()
