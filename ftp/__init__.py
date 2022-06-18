import os
from scripts.paths import check_dir_ftp, list_dir

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, BufferedIteratorProducer, _strerror
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import FilesystemError


def ftp_MLSD(self, path):
    if not self.fs.isdir(path):
        self.respond("501 No such directory.")
        return
    try:
        a = list_dir()
        listings = self.run_as_current_user(self.fs.listdir, path)
        listing = []

        for i in listings:
            pa = os.path.join(path, i).replace('\\', '/')
            for j in a:
                if pa in j:
                    listing.append(i)
                if os.path.isfile(pa):
                    pa = pa.split('/')
                    del pa[-1]
                    pa = "/".join(pa)
                if pa == j:
                        listing.append(i)
        listing = set(listing)
    except (OSError, FilesystemError) as err:
        why = _strerror(err)
        self.respond('550 %s.' % why)
    else:
        perms = self.authorizer.get_perms(self.username)
        iterator = self.fs.format_mlsx(path, listing, perms,
                                       self._current_facts)
        producer = BufferedIteratorProducer(iterator)
        self.push_dtp_data(producer, isproducer=True, cmd="MLSD")
        return path


# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions and a read-only
# anonymous user
authorizer.add_user('user', '12345', 'I:\\', perm='elradfmwMT')
authorizer.add_anonymous(os.getcwd())

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer


# handler.ftp_LIST = ftp_LIST.__get__(handler, FTPHandler)
# handler.ftp_NLST = ftp_NLST.__get__(handler, FTPHandler)
handler.ftp_MLSD= ftp_MLSD

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
