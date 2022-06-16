import os
import platform
from hashlib import sha256
from tkinter import filedialog, messagebox, Label, Button, Entry, ttk, Toplevel

if platform.system() != 'Windows':
    import subprocess


def open_path(path: str):
    """
    a cross-platform file opening
    :param path: file path
    :return: file path opening
    """

    def showerror():
        """
        :return:  Show error This folder does not exist.
        """
        messagebox.showerror(title="File Not Found", message="This folder does not exist.")

    match platform.system():
        case 'Windows':
            try:
                os.startfile(path)
            except FileNotFoundError:
                showerror()
        case 'Darwin':
            try:
                subprocess.Popen(['open', path])
            except FileNotFoundError:
                showerror()
        case _:
            try:
                subprocess.Popen(['xdg-open', path])
            except FileNotFoundError:
                showerror()


class Setting:
    def __init__(self, root, icon_window, database):
        self.database = database
        setting = Toplevel(root)
        setting.title("Setting")
        setting.geometry("600x300")
        setting.resizable(False, False)
        icon_window(setting)

        tab_control = ttk.Notebook(setting)

        self.tab_received = ttk.Frame(tab_control)
        self.tab_control_system_pas = ttk.Frame(tab_control)

        tab_control.add(self.tab_received, text="Received files")
        self._window_received()
        tab_control.add(self.tab_control_system_pas, text="Control system password")
        self._shutdown_sleep()
        tab_control.pack(expand=1, fill="both")

    def _redirect_received(self):
        """
        Saves the upload folder path to the database.
        """
        deiconiry = filedialog.askdirectory()
        if deiconiry != '':
            self.database.write_data(deiconiry, "upload")
            path_upload['text'] = deiconiry

    def _window_received(self):
        """
        settings of received files
        """
        global path_upload
        path_uploads = self.database.get_data()[3]
        Label(self.tab_received, text="Path of received files: ", font=('arial', 10, 'bold')).place(x=10, y=10)
        path_upload = Label(self.tab_received, text=path_uploads, font=('arial', 10, 'bold'), fg="blue")
        path_upload.bind("<Button-1>", lambda event, e=path_uploads: open_path(e))
        path_upload.place(x=10, y=35)
        Button(self.tab_received, text="Select a folder", font=('arial', 10, 'bold'),
               command=self._redirect_received).place(relx=0.5, rely=0.3, anchor="center")

    def _shutdown_sleep(self):
        """
        Window related to changing the shutdown password and system sleep mode
        """

        def chack_password():
            """
             Function to check the password and confirm the password and save it in the database
            """
            password = password_box.get()
            password_v = password_v_box.get()
            if password == password_v and password is not None:
                password = sha256(password.encode())
                self.database.write_data(password.hexdigest(), "password")
                messagebox.showinfo(title="successful", message="Password set successfully")
            else:
                messagebox.showerror(title="ERROR", message="Enter valid password")

        Label(self.tab_control_system_pas, text="Enter password: ", font=('arial', 10, 'bold')).place(x=10, y=10)
        Label(self.tab_control_system_pas, text="Repeat password for verification: ",
              font=('arial', 10, 'bold')).place(x=10, y=60)

        password_box = Entry(self.tab_control_system_pas, font=('arial', 10, 'bold'), show="*")
        password_box.place(x=10, y=35, width=300)
        password_v_box = Entry(self.tab_control_system_pas, font=('arial', 10, 'bold'), show="*")
        password_v_box.place(x=10, y=85, width=300)
        Button(self.tab_control_system_pas, text="Set password", font=('arial', 10, 'bold'),
               command=chack_password).place(x=215, y=130)
