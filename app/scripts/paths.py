import os

from flask import redirect

from .sqllite import Database


def edit_path_windows_other(path: str) -> str:
    """
    :param path:  Directory path
    :return: If it is Windows, it remains unchanged, in other systems / it is added to the first path
    """
    if os.name != 'nt':
        path = '/' + path
    return path


def list_file(format_file: list, path: str) -> list:
    """
    :param format_file: The desired file format, for example mp4
    :param path: The desired folder path
    :return: Returns a list of files related to the imported format
    """
    files = []
    path = edit_path_windows_other(path)
    for i in format_file:
        if i == '*':
            files = os.listdir(path)
        else:
            for name in os.listdir(path):
                if os.path.splitext(name)[1] == f'.{i}':
                    files.append(os.path.join(path, name))
    return files


def list_dir() -> str:
    """
    :return: Returns the list of folders stored in the database
    """
    database = Database()
    try:
        dirc = database.get_data()[0].split(',')
    except AttributeError:
        dirc = []
    return dirc


def _check(path: str) -> bool:
    """
   Check if the file is available through the page
   :param path: The requested file path on the page
   :return: Returns true if the file path is in the database, otherwise false
    """
    dircs = list_dir()
    path = edit_path_windows_other(path)
    status = False
    if os.path.isfile(path):
        path = path.split('/')
        del path[-1]
        path = "/".join(path)
    if path in dircs:
        status = True
    return status


def check_dir_flask(function):
    """
    Decorator If access to the directory is allowed, the function is executed; otherwise, it redirects to the path_redirect
    """
    def check(link):
        if _check(link):
            return function(link)
        else:
            return redirect('/')
    check.__name__ = function.__name__
    return check

