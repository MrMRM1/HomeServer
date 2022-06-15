import os
import platform
from time import sleep


def shutdown_sleep_thread(value):
    """
    :param value: Sleep or Shutdown
    :return: Delayed shutdown or sleep mode after 3 seconds
    """
    sleep(3)
    if value == "Sleep":
        match platform.system():
            case 'Windows':
                os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep 2")
            case 'Darwin':
                os.system("pmset sleepnow")
            case _:
                os.system("systemctl suspend")
    elif value == "Shutdown":
        if platform.system() == 'Windows':
            os.system("shutdown /s /t 2")
        else:
            os.system("shutdown -h now")