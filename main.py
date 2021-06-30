from tkinter import *
from tkinter import filedialog
from socket import socket, AF_INET, SOCK_DGRAM
from sqllite import Database
from threading import Thread
s = socket(AF_INET, SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
database = Database()
ip = s.getsockname()[0]


def path_dir():
    deiconiry = filedialog.askdirectory()
    try:
        paths = eval(database.get_data()[0])
        paths.append(deiconiry)
    except:
        paths = [deiconiry]
    database.write_data(paths)
    load_data()


def del_itms():
    try:
        list_box.delete(0, 'end')
    except :
        pass


def del_path(event):
    cs = list_box.curselection()[0]
    paths = eval(database.get_data()[0])
    del paths[cs]
    database.write_data(paths)
    load_data()


def load_data():
    try:
        del_itms()
        paths = eval(database.get_data()[0])
        for i in paths[::-1]:
            list_box.insert(0, i)
    except:
        pass


def threading_start():
    run_app.start()


def threading_stop():
    root.quit()


def run():
    button_run["state"] = "disabled"
    button_Selection["state"] = "disabled"
    port_box["state"] = "disabled"
    list_box["state"] = "disabled"
    button_stop["state"] = "normal"
    port = port_box.get()
    address_run = Label(root, text=f"Enter in the browser {ip}:{port}", font=('arial', 10, 'bold'))
    address_run.place(x=40, y=285)
    from app import app
    app.run(host=ip, port=port, debug=False)


run_app = Thread(target=run)
run_app.setDaemon(True)
root = Tk()
root.title("File sharing")
root.geometry("500x350")

root.resizable(False, False)
ip_address = Label(root, text=ip+":", font=('arial', 15, 'bold')).place(x=110, y=20)
port_box = Entry(root, font=('arial', 15, 'bold'), )
port_box.insert(END, 5050)
port_box.place(x=250, y=21, width=100)
title_list = Label(root, text="List of folders", font=('arial', 10, 'bold')).place(x=40, y=70)
button_Selection = Button(root, text="Select a folder", font=('arial', 10, 'bold'), command=path_dir)
button_Selection.place(x=360, y=60)
list_box = Listbox(root)
load_data()
list_box.bind('<Double-Button>', del_path)
list_box.place(x=40, y=100, width=425)
button_run = Button(root, text="Run", font=('arial', 10, 'bold'), command=threading_start)
button_run.place(x=430, y=280)
button_stop = Button(root, text="Stop and exit", font=('arial', 10, 'bold'), command=threading_stop)
button_stop["state"] = "disabled"
button_stop.place(x=330, y=280)
Label(root, text="About the developer: http://MrMRM.ir/", font=('arial', 8, 'bold')).place(x=40, y=320)
root.iconbitmap('icon.ico')
root.mainloop()


