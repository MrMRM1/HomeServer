import sqlite3
from pathlib import Path
from os.path import join as join_path
from os import remove
from re import fullmatch
from ast import literal_eval

from .network import port_flask

path_received = join_path(Path.home().__str__(), 'Downloads', 'HomeServerReceived')


class Database:
    def __init__(self):
        self.data = sqlite3.connect('data.db', check_same_thread=False)
        self.my_db = self.data.cursor()
        try:
            self.my_db.execute(f"SELECT * from data_user")
            data = self.my_db.fetchone()
            try:
                self.my_db.execute("SELECT * FROM users LIMIT 1")
                users_data = self.my_db.fetchone()
                if len(data) < 14 or len(users_data) < 12:
                    self.my_db.execute("SELECT * FROM users")
                    users_data = self.my_db.fetchall()
                    self.update_data_user(data, users_data)
            except (sqlite3.OperationalError, TypeError):
                self.update_data_user(data, None)

        except:
            self.my_db.execute(
                f'CREATE TABLE data_user (paths LONGTEXT NULL, port INT DEFAULT {port_flask()}, data_id DEFAULT "1" ,upload DEFAULT "{path_received}", password TEXT NULL, port_ftp INT DEFAULT 8821, ftp_server DEFAULT "0", ftp_root NULL, ftp_create_directory DEFAULT "0", ftp_store_file DEFAULT "0", run_background DEFAULT "0", login_status DEFAULT "0", admin_username TEXT NULL, admin_password TEXT NULL)')
            self.my_db.execute('INSERT INTO data_user (data_id) VALUES ("1")')
            self.data.commit()
            self.my_db.execute(f'CREATE TABLE users (id INTEGER primary key NOT NULL ,username TEXT NULL UNIQUE, password TEXT NULL, paths LONGTEXT NULL, ftp_status DEFAULT "1", video_status DEFAULT "1", audio_status DEFAULT "1",  pdf_status DEFAULT "1", receive_status DEFAULT "1",  send_status DEFAULT "1",  system_control_status DEFAULT "1",  picture_status DEFAULT "1")')
            self.my_db.execute('INSERT INTO users (ftp_status) VALUES ("1")')
            self.data.commit()

    def get_data(self):
        self.my_db.execute(f'SELECT * from data_user WHERE data_id = "1"')
        return self.my_db.fetchone()

    def write_data(self, data, data_type):
        sql = f'UPDATE data_user SET {data_type} = "{data}" WHERE data_id = "1"'
        self.my_db.execute(sql)
        self.data.commit()

    def update_data_user(self, data_user, users):
        data_user = list(data_user)
        if fullmatch(r'^\[.*]$', data_user[0]):
            data_user[0] = ','.join(literal_eval(data_user[0]))
        self.data.close()
        remove('data.db')
        key = ['paths', 'port', 'data_id', 'upload', 'password', 'port_ftp', 'ftp_server', 'ftp_root',
               'ftp_create_directory', 'ftp_store_file', 'run_background', 'login_status', 'admin_username', 'admin_password']
        self.__init__()
        for i, j in zip(data_user, key):
            self.write_data(i, j)
        if users is not None:
            self.update_users(users)

    def update_users(self, data):
        key = ['username', 'password', 'paths', 'ftp_status', 'video_status', 'audio_status', 'pdf_status',
               'receive_status', 'send_status', 'system_control_status', 'picture_status']
        for s in data:
            s = list(s)
            for i, j in zip(s[1:], key):
                self.write_users_data(i, j, s[0])

    def get_user_data(self, username: str):
        self.my_db.execute(f'SELECT * from users WHERE username = "{username}"')
        return self.my_db.fetchone()

    def write_users_data(self, data: str, data_type: str, user_id: int):
        sql = f'UPDATE users SET {data_type} = "{data}" WHERE id = {user_id}'
        self.my_db.execute(sql)
        self.data.commit()
