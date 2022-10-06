import os

from app.scripts.paths import list_dir
from app.scripts.sqllite import database


def listdir(self, root: str, username: str) -> list:
    """
    It takes the root and returns the list of allowed directories
    :param username: username
    :param root:  path root
    :return: the list of allowed directories
    """
    allowed = list_dir(ftp=True, username=username)
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


def get_root(advance: int = 2, username: str = None) -> list:
    """
    It extracts roots from inside the paths as much as it advances
    :param username: username
    :param advance: amount of advance
    :return: List of roots
    examole :
        advance = 2
        allowlist = ['C:\\user\\Desktop', 'E:\\Download\\Video\\Short', 'E:\\Music']

        return: ['C:\\user', 'E:\\Download', 'E:\\Music', 'C:\\', 'E:\\']
    """
    allowlist = list_dir(ftp=True, username=username)
    roots = []

    def appdend_root(index=1):
        for i in allowlist:
            root = '/'.join(i.split('/')[:index]) + '/'
            if root not in roots:
                roots.append(root)
        return roots
    for i in range(1, advance + 1):
        appdend_root(i)
    return roots


def allowed_dir(root: str, username: str) -> bool:
    """
    Checks if path access is allowed
    :param username: username
    :param root: path
    :return: bool
    """
    allowed_list = list_dir(ftp=True, username=username)
    root = root.replace('\\', '/')
    if os.path.isfile(root):
        if os.path.dirname(root) in allowed_list:
            return True
    else:
        for j in allowed_list:
            if root in j:
                return True
    return False


def chdir(self, path, username):
    """
    If the access is allowed, the program continues, otherwise it returns an error.
    """
    if allowed_dir(path, username):
        os.chdir(path)
        self.cwd = self.fs2ftp(path)
    else:
        raise OSError(1, 'Operation not permitted')


def path_append(data: str, path: str) -> str:
    list_path = data.split(',')
    list_path.append(path)
    return ','.join(list_path)


def mkdir(self, path, username):
    """Create the specified directory."""
    allowed_list = list_dir(ftp=True, username=username)
    path = path.replace('\\', '/')
    if os.path.dirname(path) in allowed_list:
        os.mkdir(path)
        list_path = database.get_data()[0].split(',')
        list_path.append(path)
        database.write_data(','.join(list_path), 'paths')
    else:
        raise OSError(1, 'Operation not permitted')


def open_fs(self, filename, mode, username):
    """
    If the access is allowed, the program continues, otherwise it returns an error.
    """
    allowed_list = list_dir(ftp=True, username=username)
    if os.path.dirname(filename.replace('\\', '/')) in allowed_list:
        return open(filename, mode)
    else:
        raise OSError(1, 'Operation not permitted')
