import os
import sys
import tempfile
import subprocess
import platform


def windows_get_process() -> list:
    """
    Receiving running programs with the same name as the program and extracting their IDs in windows
    :return: A list of program IDs
    """
    app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    cmd = 'Powershell "Get-Process | select ProcessName,Id"'
    pop = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ids = []
    for i in pop.stdout:
        data = i.decode().rstrip().split(' ')
        if data[0] == app_name:
            ids.append(data[-1])
    return ids


def windows_kill_process(id_process):
    """
    :param id_process:  process ID
    :return: Kills the process with the ID in windows
    """
    cmd = f'Powershell "Stop-Process -Id {id_process}"'
    pop = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return pop.stdout


def linux_get_process() -> list:
    """
    Receiving running programs with the same name as the program and extracting their IDs in linux
    :return: A list of program IDs
    """
    app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    cmd = "ps -x"
    pop = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ids = []
    for i in pop.stdout:
        data = i.decode().rstrip().split(' ')
        if os.path.splitext(os.path.basename(data[-1]))[0] == app_name:
            for j in data:
                try:
                    ids.append(str(int(j)))
                    break
                except:
                    pass
    return ids


def linux_kill_process(id_process):
    """
    :param id_process:  process ID
    :return: Kills the process with the ID in windows
    """
    cmd = f'kill {id_process}'
    pop = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return pop.stdout


def get_process() -> list:
    """
    Management of receiving processes in different systems
    """
    data = None
    match platform.system():
        case 'Windows':
            data = windows_get_process()
        case _:
            data = linux_get_process()
    return data


class SingleInstance(object):

    def __init__(self):
        self.read_file = []
        self.already_running = False
        self.basename = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '-data.temp'
        self.lockfile = os.path.normpath(tempfile.gettempdir() + '/' + self.basename)
        try:
            with open(self.lockfile, 'r') as file:
                for j in file.read().split(' ').copy():
                    if j in get_process():
                        self.read_file.append(j)
            if len(self.read_file) == 0:
                self._file_write()
            else:
                self.already_running = True
        except FileNotFoundError:
            self._file_write()

    def _file_write(self):
        with open(self.lockfile, 'w') as file:
            file.write(' '.join(get_process()))

    def update(self):
        self._file_write()

    def __iter__(self):
        return iter(self.read_file)

    def __bool__(self):
        return len(self.read_file) > 0

    def kill_process(self, id_process):
        """
        :param id_process: process ID
        :return: Management of application keying in different systems
        """
        data = None
        match platform.system():
            case 'Windows':
                data = windows_kill_process(id_process)
            case _:
                data = linux_kill_process(id_process)
        self.update()
        return data
