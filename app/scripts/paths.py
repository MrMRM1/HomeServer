import os
import time

from flask import abort, request
from flask_login import current_user

from .sqllite import database


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


def list_dir(ftp=False, username=None) -> list:
    """
    :return: Returns the list of folders stored in the database
    """
    def data_to_list(data: str) -> list:
        return data.split(',')

    def get_path_username(user):
        if user == user_data[12]:
            return data_to_list(user_data[0])
        else:
            return data_to_list(database.get_user_data(user)[3])

    user_data = database.get_data()
    try:
        if ftp:
            return get_path_username(username)
        else:
            if user_data[11] == '1':
                try:
                    username = current_user.username
                except AttributeError:
                    secret_data = database.get_secret_data(request.args['secret'])
                    if time.time() >= secret_data[2]:
                        return []
                    username = secret_data[3]
                return get_path_username(username)
            else:
                return data_to_list(user_data[0])
    except AttributeError:
        return []


def check_path(path: str) -> bool:
    """
   Check if the file is available through the page
   :param path: The requested file path on the page
   :return: Returns true if the file path is in the database, otherwise false
    """
    dircs = list_dir()
    path = edit_path_windows_other(path)
    status = False
    if os.path.isfile(path):
        path = os.path.dirname(path)
    if path in dircs:
        status = True
    return status


def check_dir_flask(function):
    """
    Decorator If access to the directory is allowed, the function is executed; otherwise, it redirects to the path_redirect
    """
    def check(link):
        if check_path(link):
            return function(link)
        else:
            return abort(404)
    check.__name__ = function.__name__
    return check

