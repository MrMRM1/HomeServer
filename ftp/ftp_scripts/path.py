import os
from scripts.paths import list_dir
from scripts.sqllite import Database


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


def get_root():
    allowlist = list_dir()
    roots = []

    def appdend_root(index=1):
        for i in allowlist:
            root = '/'.join(i.split('/')[:index]) + '/'
            if root not in roots:
                roots.append(root)
        return roots
    appdend_root()
    appdend_root(2)
    return roots


def allowed_dir(root):
    allowed_list = list_dir()
    list_dir_root = os.listdir(root)
    if list_dir_root:
        for i in list_dir_root:
            path = os.path.join(root, i).replace('\\', '/')
            for j in allowed_list:
                if path in j:
                    return True
                else:
                    if os.path.isfile(path):
                        if root.replace('\\', '/') == j:
                            return True
    else:
        if root.replace('\\', '/') in allowed_list:
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
    print(list_dir())
    allowed_list = list_dir()
    path_split = path.replace('\\', '/').split('/')
    if '/'.join(path_split[:-1]) in allowed_list:
        database = Database()
        os.mkdir(path)
        list_path = database.get_data()[0].split(',')
        list_path.append('/'.join(path_split))
        database.write_data(','.join(list_path), 'paths')
    else:
        raise OSError(1, 'Operation not permitted')