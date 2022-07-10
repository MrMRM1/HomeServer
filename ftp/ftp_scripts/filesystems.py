import os

from scripts.paths import list_dir
from scripts.sqllite import Database


def listdir(self, root: str) -> list:
    """
    It takes the root and returns the list of allowed directories
    :param root:  path root
    :return: the list of allowed directories
    """
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


def get_root(advance: int = 2) -> list:
    """
    It extracts roots from inside the paths as much as it advances
    :param advance: amount of advance
    :return: List of roots
    examole :
        advance = 2
        allowlist = ['C:\\user\\Desktop', 'E:\\Download\\Video\\Short', 'E:\\Music']

        return: ['C:\\user', 'E:\\Downloadt', 'E:\\Music', 'C:\\', 'E:\\']
    """
    allowlist = list_dir()
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


def allowed_dir(root):
    allowed_list = list_dir()
    root = root.replace('\\', '/')
    if os.path.isfile(root):
        if os.path.dirname(root) in allowed_list:
            return True
    else:
        for j in allowed_list:
            if root in j:
                return True
    return False


def chdir(self, path):
    if allowed_dir(path):
        os.chdir(path)
        self.cwd = self.fs2ftp(path)
    else:
        raise OSError(1, 'Operation not permitted')


def mkdir(self, path):
    """Create the specified directory."""
    allowed_list = list_dir()
    path = path.replace('\\', '/')
    if os.path.dirname(path) in allowed_list:
        database = Database()
        os.mkdir(path)
        list_path = database.get_data()[0].split(',')
        list_path.append(path)
        database.write_data(','.join(list_path), 'paths')
    else:
        raise OSError(1, 'Operation not permitted')


def open_fs(self, filename, mode):
    allowed_list = list_dir()
    if os.path.dirname(filename.replace('\\', '/')) in allowed_list:
        return open(filename, mode)
    else:
        raise OSError(1, 'Operation not permitted')