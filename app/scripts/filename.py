import os.path
from os import listdir
from re import findall


def pathfile(path: str, filename: str) -> str:
    """
    :param path: File path
    :param filename: File Name
    :return: the new path using the renamefile function.
    """
    return f"{path}/{renamefile(path, filename)}"


def renamefile(path: str, filename: str) -> str:
    """
    :param path: File path
    :param filename: File Name
    :return: If the filename is not a duplicate, The name is returned without change,
    otherwise a new name is created with the help of the edit_name function.
    """
    if filename in listdir(path):
        filename = edit_name(path, filename)
    return filename


def edit_name(path: str, filename: str) -> str:
    """
    :param path: File path
    :param filename: File Name
    :return: Adds a number to the end of the filename to make the filename unique.
    """
    filename = os.path.splitext(filename)
    file_type = filename[1]
    name = filename[0]
    check_name = findall("\(\d*\)$", name)
    if check_name:
        number = int(check_name[0][1:len(check_name[0])-1])
        name = renamefile(path, f'{name[:-len(check_name[0])]}({number+1}){file_type}')
    else:
        name = renamefile(path, f'{name}(1){file_type}')
    return name
