from tkinter import *
from tkinter import filedialog, messagebox
from socket import socket, AF_INET, SOCK_DGRAM
from sqllite import Database
from threading import Thread
from webbrowser import open_new
from urllib.request import urlopen, Request
from json import loads
import re
v = 111
database = Database()
connected_network = False

try:
    ico = '../static/icon.ico'
    open(ico, 'r')
except:
    ico = 'icon.ico'
    open(ico, 'r')

try:
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    connected_network = True
except:
    root = Tk()
    root.withdraw()
    root.title("Home Server")
    root.geometry("0x0")
    root.resizable(False, False)
    messagebox.showerror(title="ERROR", message="You are not connected to the local network")
    root.deiconify()


def check_update():
    try:
        req = Request(url="http://mrmrm.ir/update/File%20Sharing.json", headers={'User-Agent': 'Mozilla/5.0'})
        data = loads(urlopen(req).read())
        if data['version']['v'] == v:
            messagebox.showinfo(title="updated", message="You are using the latest version")
        elif data['version']['v'] > v:
            message = "New version available, do you want to download? \nabout this update: \n"
            message += data['version']['changes']
            ask_update = messagebox.askquestion(title="New version available", message=message)
            if ask_update == 'yes':
                open_new(data['version']['link'])
    except:
        messagebox.showerror(title="ERROR", message="No connection to the server")


def path_dir():
    deiconiry = filedialog.askdirectory()
    if re.fullmatch(r'.:\/', deiconiry):
        messagebox.showwarning(title="WARNING", message="You are not allowed to select a drive, you must select a folder")
    else:
        try:
            paths = eval(database.get_data()[0])
            if deiconiry in paths:
                pass
            else:
                paths.append(deiconiry)
        except:
            paths = [deiconiry]
        database.write_data(paths, "paths")
        load_data()


def path_upload():
    CUL_window.destroy()
    deiconiry = filedialog.askdirectory()
    database.write_data(deiconiry, "upload")
    CUL()


def CUL():
    global CUL_window
    CUL_window = Toplevel(root)
    CUL_window.geometry("500x70")
    CUL_window.resizable(False, False)
    path_uploads = database.get_data()[3]
    Label(CUL_window, text="Upload location: "+path_uploads, font=('arial', 10, 'bold')).place(x=10, y=10)
    Button(CUL_window, text="Close", font=('arial', 10, 'bold'), command=CUL_window.destroy).place(x=435, y=36)
    selec_path = Button(CUL_window, text="Select a folder", font=('arial', 10, 'bold'), command=path_upload)
    selec_path.place(x=332, y=36)
    CUL_window.iconbitmap(ico)


def del_itms():
    try:
        list_box.delete(0, 'end')
    except :
        pass


def del_path(event):
    cs = list_box.curselection()[0]
    paths = eval(database.get_data()[0])
    del paths[cs]
    database.write_data(paths, "paths")
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
    global run_app
    run_app = Thread(target=run)
    run_app.start()


def threading_stop():
    address_run.place_forget()
    port = port_box.get()
    open_new(f"http://{ip}:{port}/shutdown")
    button_run["state"] = "normal"
    button_Selection["state"] = "normal"
    port_box["state"] = "normal"
    list_box["state"] = "normal"
    button_stop["state"] = "disabled"
    run_app.join()
    write_port(port)


def run():
    global address_run
    port = port_box.get()
    button_run["state"] = "disabled"
    button_Selection["state"] = "disabled"
    port_box["state"] = "disabled"
    list_box["state"] = "disabled"
    button_stop["state"] = "normal"
    address_run = Label(root, text=f"{ip}:{port}", font=('arial', 10, 'bold'), fg="blue")
    address_run.bind("<Button-1>", lambda e: open_new(f"http://{ip}:{port}"))
    address_run.place(x=175, y=265)
    from app import app
    app.run(host=ip, port=port, debug=False)


def write_port(port):
    return database.write_data(port, "port")


def port():
    try:
        data = database.get_data()[1]
        if data is None:
            raise NameError('None data')
        else:
            port_box.insert(END, data)
    except:
        port_box.insert(END, 5050)


if connected_network:
    root = Tk()
    root.title("Home Server")
    root.geometry("500x350")
    root.resizable(False, False)

    menubar = Menu(root)
    #file menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Change upload location", command=CUL)
    menubar.add_cascade(label="File", menu=filemenu)
    # help menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About developer", command=lambda: open_new('http://MrMRM.ir'))
    helpmenu.add_command(label="Github", command=lambda: open_new('https://github.com/MrMRM1/HomeServer'))
    helpmenu.add_command(label="Donate", command=lambda: open_new('http://MrMRM.ir/donate'))
    helpmenu.add_separator()
    helpmenu.add_command(label="Check Update", command=check_update)
    menubar.add_cascade(label="Help", menu=helpmenu)

    ip_address = Label(root, text=ip+":", font=('arial', 15, 'bold')).place(x=100, y=20)
    port_box = Entry(root, font=('arial', 15, 'bold'), )
    port()
    port_box.place(x=260, y=21, width=100)
    title_list = Label(root, text="List of folders (Double click to delete the item)", font=('arial', 10, 'bold')).place(x=40, y=65)
    button_Selection = Button(root, text="Select a folder", font=('arial', 10, 'bold'), command=path_dir)
    button_Selection.place(x=360, y=60)
    list_box = Listbox(root)
    load_data()
    list_box.bind('<Double-Button>', del_path)
    list_box.place(x=40, y=100, width=425, height= 150)
    button_run = Button(root, text="Run", font=('arial', 10, 'bold'), command=threading_start)
    button_run.place(x=430, y=260)
    button_stop = Button(root, text="Stop", font=('arial', 10, 'bold'), command=threading_stop)
    button_stop["state"] = "disabled"
    button_stop.place(x=390, y=260)
    Label(root, text=f"Enter in the browser:", font=('arial', 10, 'bold')).place(x=40, y=265)
    root.iconbitmap(ico)
    root.config(menu=menubar)
    root.mainloop()
else:
    pass

input()


