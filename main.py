from tkinter import *
from tkinter import filedialog, messagebox
from scripts.sqllite import Database
from threading import Thread
from webbrowser import open_new
from urllib.request import urlopen, Request
from urllib.error import URLError
from json import loads
import os
import re
from app import app
from scripts.setting_windows import Setting
from scripts.network import port_flask, get_ip
from ftp import ftp_server

from gevent.pywsgi import WSGIServer


v = 5
database = Database()
connected_network = False
ip = ''


def icon_window(window):
    """
    :param window: Display window
    :return: Set the icon for the desired window
    """
    window.iconbitmap(os.path.join(os.path.dirname(__file__), "static/icon/icon.ico"))


def check_update():
    """
    This function checks if updates are available
    :return: If an update is available, a window with a download link will be displayed, otherwise your message you are
     using the latest version will be displayed.
    """
    try:
        req = Request(url=f"http://mrmrm.ir/update/Home%20Server.php?v={v}", headers={'User-Agent': 'Mozilla/5.0'})
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
        try:
            paths = eval(database.get_data()[0])
            if directory not in paths:
                for i in list_folders(directory):
                    if i not in paths:
                        paths.append(i)
        except:
            paths = [directory]
        database.write_data(paths, "paths")
        load_data()


def list_folders(path):
    """
    :param path: Folder path
    :return: The path of the folders inside the given path
    """
    a = []
    b = [x[0] for x in os.walk(path)]
    for i in b:
        i = i.split('\\')
        i = '/'.join(i)
        a.append(i)
    return a


def del_itms():
    """
    Delete a folder path from the folder list
    """
    try:
        list_box.delete(0, 'end')
    except:
        pass


def del_path(*args):
    """
    Function to delete the selected path from the database and the list of folders
    """
    cs = list_box.curselection()[0]
    paths = eval(database.get_data()[0])
    del paths[cs]
    database.write_data(paths, "paths")
    load_data()


def load_data():
    """
    Function to get the path of folders from the database and add them to the list
    """
    try:
        del_itms()
        paths = eval(database.get_data()[0])
        for i in paths[::-1]:
            list_box.insert(0, i)
    except:
        pass


def threading_start():
    """
    Function to execute the flask program in the form of threading
    """
    global run_app
    global ftp_app
    run_app = Thread(target=run)
    run_app.start()
    ftp_app = Thread(target=run_ftp)
    ftp_app.start()
    button_run["state"] = "disabled"
    button_Selection["state"] = "disabled"
    port_box["state"] = "disabled"
    list_box["state"] = "disabled"
    button_stop["state"] = "normal"


def threading_stop():
    """
    Function to stop the flask program as threading
    """
    address_run.place_forget()
    address_run_ftp.place_forget()
    port_app = port_box.get()
    http_server.stop(timeout=2)
    if database.get_data()[6] == 1:
        ftp_server_control.stop()
        ftp_app.join()
    button_run["state"] = "normal"
    button_Selection["state"] = "normal"
    port_box["state"] = "normal"
    list_box["state"] = "normal"
    button_stop["state"] = "disabled"
    run_app.join()
    write_port(port_app)


def run():
    """
    Disable different sections of the main window and run the flask program
    """
    global address_run
    global http_server
    port_app = port_box.get()
    if port_app == '80':
        address_app = str(ip)
    else:
        address_app = f"{ip}:{port_app}"
    address_run = Label(root, text=address_app, font=('arial', 10, 'bold'), fg="blue")
    address_run.bind("<Button-1>", lambda e: open_new(f"http://{address_app}"))
    address_run.place(x=175, y=265)
    http_server = WSGIServer((ip, int(port_app)), app)
    http_server.serve_forever()


def run_ftp():
    global address_run_ftp
    global ftp_server_control
    data = database.get_data()
    if data[6] == '0':
        address_run_ftp = 'disable'
        address_run_ftp = Label(root, text=address_run_ftp, font=('arial', 10, 'bold'), fg="blue")
        address_run_ftp.place(x=125, y=290)
    else:
        address_run_ftp = f'Host: {ip}  Port: {data[5]}  Login anonymously'
        address_run_ftp = Label(root, text=address_run_ftp, font=('arial', 10, 'bold'), fg="blue")
        address_run_ftp.place(x=125, y=290)
        ftp_server_control = ftp_server(data, ip, os.path.realpath(data[7]))
        ftp_server_control.serve_forever(handle_exit=False)


def write_port(port_app):
    """
    :param port_app: Flask program execution port
    Save the port to the database
    """
    database.write_data(port_app, "port")


def port():
    """
    Get the port stored in the database and display it in the main window
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
    if messagebox.askquestion("Quit", "Do you want to quit?\nThis stops the program") == "yes":
        if button_run["state"] == "disabled":
            threading_stop()
        root.destroy()


def open_setting():
    if button_run["state"] == "normal":
        Setting(root, icon_window, database)
    else:
        messagebox.showerror("Error", message="You can not change the settings while running the program. Stop the program first, then try again.")


if __name__ == '__main__':
    try:
        ip = get_ip()
        connected_network = True
    except OSError:
        root = Tk()
        root.withdraw()
        root.title("Home Server")
        root.geometry("0x0")
        root.resizable(False, False)
        icon_window(root)
        messagebox.showerror(title="ERROR", message="You are not connected to any networks")
        root.deiconify()

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
        helpmenu.add_command(label="About developer", command=lambda: open_new('http://MrMRM.ir'))
        helpmenu.add_command(label="Github", command=lambda: open_new('https://github.com/MrMRM1/HomeServer'))
        helpmenu.add_command(label="Donate", command=lambda: open_new('http://MrMRM.ir/donate'))
        helpmenu.add_separator()
        helpmenu.add_command(label="Check Update", command=check_update)
        menubar.add_cascade(label="Help", menu=helpmenu)
        Label(root, text=ip + ":", font=('arial', 15, 'bold')).place(x=100, y=20)
        port_box = Entry(root, font=('arial', 15, 'bold'), )
        port()
        port_box.place(x=260, y=21, width=100)
        title_list = Label(root, text="List of folders (Double click to delete the item)", font=('arial', 10, 'bold'))
        title_list.place(x=40, y=65)
        button_Selection = Button(root, text="Select a folder", font=('arial', 10, 'bold'), command=path_dir)
        button_Selection.place(x=360, y=60)
        list_box = Listbox(root)
        load_data()
        list_box.bind('<Double-Button>', del_path)
        list_box.place(x=40, y=100, width=425, height=150)
        button_run = Button(root, text="Run", font=('arial', 10, 'bold'), command=threading_start)
        button_run.place(x=430, y=260)
        button_stop = Button(root, text="Stop", font=('arial', 10, 'bold'), command=threading_stop)
        button_stop["state"] = "disabled"
        button_stop.place(x=390, y=260)
        Label(root, text=f"Enter in the browser:", font=('arial', 10, 'bold')).place(x=40, y=265)
        Label(root, text=f"FTP Server :", font=('arial', 10, 'bold')).place(x=40, y=290)
        icon_window(root)
        root.config(menu=menubar)
        root.mainloop()
