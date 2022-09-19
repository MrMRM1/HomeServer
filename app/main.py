import os
try:
    import sys
    sys.path.append('/'.join(os.path.dirname(sys.modules['__main__'].__file__).split('/')[:-1]))
except:
    pass
import re
from _tkinter import TclError
from json import loads
from threading import Thread
from tkinter import *
from tkinter import filedialog, messagebox
from urllib.error import URLError
from urllib.request import urlopen, Request
from webbrowser import open_new

from gevent.pywsgi import WSGIServer

from web_app import app
from ftp import ftp_server
from scripts.network import port_flask, get_ip
from scripts.setting_windows import Setting, check_port
from scripts.sqllite import database
from scripts.already_running import SingleInstance
from scripts.paths import add_path_database, write_paths

v = 6
connected_network = False
ip = ''


def icon_window(window):
    """
    :param window: Display window
    :return: Set the icon for the desired window
    """
    try:
        window.iconbitmap(os.path.join(os.path.dirname(__file__), "static/icon/icon.ico"))
    except TclError:
        pass


def check_update():
    """
    This function checks if updates are available
    :return: If an update is available, a window with a download link will be displayed, otherwise your message you are
     using the latest version will be displayed.
    """
    try:
        req = Request(url=f"https://mrmrm.ir/update/Home%20Server.php?v={v}", headers={'User-Agent': 'Mozilla/5.0'})
        data = loads(urlopen(req).read())
        if data['changes'] == '':
            messagebox.showinfo(title="updated", message="You are using the latest version")
        else:
            message = "New version available, do you want to download? \nabout this update: \n"
            changes = data['changes'].split('\\n')
            message += '\n'.join(changes)
            ask_update = messagebox.askquestion(title="New version available", message=message)
            if ask_update == 'yes':
                open_new(data['link'])
    except URLError:
        messagebox.showerror(title="ERROR", message="No connection to the server")


def path_dir():
    """
    This function is called when selecting a new route, Its task is to add new folders to the list of folders and save
    the paths in the database
    :return: Update the list of folders
    """
    directory = filedialog.askdirectory()
    if re.fullmatch(r'.:/', directory):
        messagebox.showwarning(title="WARNING",
                               message="You are not allowed to select a drive, you must select a folder")
    else:
        add_path_database(directory)
        load_data()


def path_clear():
    if messagebox.askyesno('Delete all paths', 'All the paths you have added will be deleted. Are you sure?'):
        database.write_data('', 'paths')
        load_data()


def del_itms():
    """
    :return: Delete a folder path from the folder list
    """
    try:
        list_box.delete(0, 'end')
    except:
        pass


def write_paths(paths):
    """
    :param paths: The path to be stored in the database
    :return: Delete the empty path and save the path in the database
    """
    if '' in paths:
        paths.remove('')
    database.write_data(','.join(paths), "paths")


def del_path(*args):
    """
    :return: Function to delete the selected path from the database and the list of folders
    """
    try:
        cs = list_box.curselection()[0]
        paths = database.get_data()[0].split(',')
        del paths[cs]
        write_paths(paths)
        load_data()
    except IndexError:
        pass


def load_data():
    """
    :return: Function to get the path of folders from the database and add them to the list
    """
    try:
        del_itms()
        paths = database.get_data()[0].split(',')
        for i in paths[::-1]:
            list_box.insert(0, i)
    except:
        pass


def threading_start():
    """
    :return: Function to execute the flask program in the form of threading
    """
    global run_app
    global ftp_app
    port_app = check_port(port_box.get())
    if port_app != '':
        run_app = Thread(target=run, args=(port_app,))
        run_app.start()
        ftp_app = Thread(target=run_ftp)
        ftp_app.start()
        button_run["state"] = "disabled"
        button_Selection["state"] = "disabled"
        button_clear["state"] = "disabled"
        port_box["state"] = "disabled"
        list_box["state"] = "disabled"
        button_stop["state"] = "normal"


def threading_stop():
    """
    :return: Function to stop the flask program as threading
    """
    address_run.place_forget()
    address_run_ftp.place_forget()
    http_server.stop(timeout=2)
    if database.get_data()[6] == '1':
        ftp_server_control.close_all()
        ftp_app.join(1)
    button_run["state"] = "normal"
    button_Selection["state"] = "normal"
    button_clear["state"] = "normal"
    port_box["state"] = "normal"
    list_box["state"] = "normal"
    button_stop["state"] = "disabled"
    run_app.join()
    load_data()


def run(port_app):
    """
    :param port_app: Port for the program to run
    :return: Disable different sections of the main window and run the flask program
    """
    global address_run
    global http_server
    if port_app == '80':
        address_app = str(ip)
    else:
        address_app = f"{ip}:{port_app}"
    address_run = Label(root, text=address_app, font=('arial', 10, 'bold'), fg="blue")
    address_run.bind("<Button-1>", lambda e: open_new(f"http://{address_app}"))
    address_run.place(x=175, y=265)
    database.write_data(port_app, "port")
    http_server = WSGIServer((ip, int(port_app)), app)
    http_server.serve_forever()


def run_ftp():
    """
    :return: According to the settings of the ftp server, it turns on
    """
    global address_run_ftp
    global ftp_server_control
    data = database.get_data()
    if data[6] == '0':
        address_run_ftp = 'disable'
        address_run_ftp = Label(root, text=address_run_ftp, font=('arial', 10, 'bold'), fg="blue")
        address_run_ftp.place(x=125, y=290)
    else:
        address_run_ftp = f'Host: {ip}  Port: {data[5]}'
        if data[11] == '0':
            address_run_ftp += '  Login anonymously'
        address_run_ftp = Label(root, text=address_run_ftp, font=('arial', 10, 'bold'), fg="blue")
        address_run_ftp.place(x=125, y=290)
        ftp_server_control = ftp_server(data, ip)
        ftp_server_control.serve_forever(handle_exit=False)


def port():
    """
    :return: Get the port stored in the database and display it in the main window
    """
    try:
        data = database.get_data()[1]
        if data is None:
            raise NameError('None data')
        else:
            port_box.insert(END, data)
    except NameError:
        port_box.insert(END, port_flask())


def delete_window():
    """
    :return: Stops or hides the program according to the settings
    """
    if database.get_data()[10] == "0":
        if button_stop["state"] == "disabled":
            root.destroy()
        elif messagebox.askquestion("Quit", "Do you want to quit?\nThis stops the program") == "yes":
            if button_run["state"] == "disabled":
                threading_stop()
            root.destroy()
    else:
        root.destroy()


def open_setting():
    """
    :return: Open the settings window
    """
    if button_run["state"] == "normal":
        Setting(root, icon_window, database)
    else:
        messagebox.showerror("Error",
                             message="You can not change the settings while running the program. Stop the program first, then try again.")


if __name__ == '__main__':
    try:
        # This feature works in the output file (.exe, ...)
        a_running = SingleInstance()
        if a_running:
            ask = messagebox.askyesno(title='HomeServer is Already running',
                                      message="A version of the program is running, do you want to stop it?")
            if ask:
                for i in a_running:
                    a_running.kill_process(i)
            else:
                raise NameError
        ip = get_ip()
        connected_network = True
    except OSError:
        messagebox.showerror(title="HomeServer ERROR", message="You are not connected to any networks")
    except NameError:
        pass
    if connected_network:
        root = Tk()
        root.title("Home Server")
        root.geometry("500x350")
        root.resizable(False, False)
        root.protocol("WM_DELETE_WINDOW", delete_window)
        menubar = Menu(root)
        # file menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Setting", command=open_setting)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=delete_window)
        menubar.add_cascade(label="File", menu=filemenu)
        # help menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About developer", command=lambda: open_new('https://MrMRM.ir'))
        helpmenu.add_command(label="Github", command=lambda: open_new('https://github.com/MrMRM1/HomeServer'))
        helpmenu.add_command(label="Donate", command=lambda: open_new('https://MrMRM.ir/donate'))
        helpmenu.add_separator()
        helpmenu.add_command(label="Check Update", command=check_update)
        menubar.add_cascade(label="Help", menu=helpmenu)
        Label(root, text=ip + ":", font=('arial', 15, 'bold')).place(x=100, y=20)
        port_box = Entry(root, font=('arial', 15, 'bold'), )
        port()
        port_box.place(x=260, y=21, width=100)
        title_list = Label(root, text="List of folders (Double click to delete the item)", font=('arial', 10, 'bold'))
        title_list.place(x=40, y=65)
        button_Selection = Button(root, text="Add folder", font=('arial', 10, 'bold'), command=path_dir)
        button_Selection.place(x=332, y=60)
        button_clear = Button(root, text="Clear", font=('arial', 10, 'bold'), command=path_clear)
        button_clear.place(x=425, y=60)
        list_box = Listbox(root)
        load_data()
        list_box.bind('<Double-Button>', del_path)
        list_box.place(x=40, y=100, width=425, height=150)
        button_run = Button(root, text="Run", font=('arial', 10, 'bold'), command=threading_start)
        button_run.place(x=430, y=260)
        button_stop = Button(root, text="Stop", font=('arial', 10, 'bold'), command=threading_stop)
        button_stop["state"] = "disabled"
        button_stop.place(x=375, y=260)
        Label(root, text=f"Enter in the browser:", font=('arial', 10, 'bold')).place(x=40, y=265)
        Label(root, text=f"FTP Server :", font=('arial', 10, 'bold')).place(x=40, y=290)
        icon_window(root)
        root.config(menu=menubar)
        root.mainloop()
