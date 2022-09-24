import sqlite3
from pathlib import Path
from os.path import join as join_path
from os import remove
from re import fullmatch
from ast import literal_eval
import time

from .network import port_flask
from app.admin.scripts.secret_generator import random_token_url

path_received = join_path(Path.home().__str__(), 'Downloads', 'HomeServerReceived')


class Database:
    def __init__(self):
        self.data = sqlite3.connect('data.db', check_same_thread=False)
        self.my_db = self.data.cursor()
        try:
            data = self.fetchone(f"SELECT * from data_user")
            try:
                users_data = self.fetchone("SELECT * FROM users LIMIT 1")
                if len(data) < 15 or len(users_data) < 15:
                    self.my_db.execute("SELECT * FROM users")
                    users_data = self.my_db.fetchall()
                    self.update_data_app(data, users_data)
                try:
                    self.fetchone("SELECT * from secrets")
                except (sqlite3.OperationalError, TypeError):
                    self.update_data_app(data, users_data)

            except (sqlite3.OperationalError, TypeError):
                self.update_data_app(data, None)

        except sqlite3.OperationalError:
            self.my_db.execute(
                f'CREATE TABLE data_user (paths LONGTEXT NULL, port INT DEFAULT {port_flask()}, data_id DEFAULT "1" ,upload DEFAULT "{path_received}", password TEXT NULL, port_ftp INT DEFAULT 8821, ftp_server DEFAULT "0", ftp_root NULL, ftp_create_directory DEFAULT "0", ftp_store_file DEFAULT "0", run_background DEFAULT "0", login_status DEFAULT "0", admin_username TEXT NULL, admin_password TEXT NULL, guest_status DEFAULT "0")')
            self.my_db.execute('INSERT INTO data_user (data_id) VALUES ("1")')
            self.my_db.execute(f'CREATE TABLE users (id INTEGER primary key NOT NULL ,username TEXT NULL UNIQUE, password TEXT NULL, paths LONGTEXT NULL, ftp_status DEFAULT "1", video_status DEFAULT "1", audio_status DEFAULT "1",  pdf_status DEFAULT "1", receive_status DEFAULT "1",  send_status DEFAULT "1",  system_control_status DEFAULT "1",  picture_status DEFAULT "1", ftp_create_directory DEFAULT "0", ftp_store_file DEFAULT "0", ftp_root TEXT NULL)')
            self.my_db.execute('INSERT INTO users (username, receive_status, system_control_status) VALUES ("guest", "0", "0")')
            self.my_db.execute(f'CREATE TABLE secrets (secret LONGTEXT NOT NULL UNIQUE , link TEXT NOT NULL, time DATE NOT NULL, username TEXT NOT NULL, status DEFAULT "1")')
            self.data.commit()

    def sql_commit(self, sql):
        try:
            self.my_db.execute(sql)
            self.data.commit()
        except sqlite3.OperationalError:
            # database is locked
            data = self.fetchone(f"SELECT * from data_user")
            self.my_db.execute("SELECT * FROM users")
            users_data = self.my_db.fetchall()
            self.update_data_app(data, users_data)

    def fetchone(self, sql):
        self.my_db.execute(sql)
        return self.my_db.fetchone()

    def get_data(self):
        return self.fetchone(f'SELECT * from data_user WHERE data_id = "1"')

    def write_data(self, data, data_type):
        self.sql_commit(f'UPDATE data_user SET {data_type} = "{data}" WHERE data_id = "1"')

    def update_data_app(self, data_user, users):
        data_user = list(data_user)
        if fullmatch(r'^\[.*]$', data_user[0]):
            data_user[0] = ','.join(literal_eval(data_user[0]))
        self.data.close()
        remove('data.db')
        key = ['paths', 'port', 'data_id', 'upload', 'password', 'port_ftp', 'ftp_server', 'ftp_root',
               'ftp_create_directory', 'ftp_store_file', 'run_background', 'login_status', 'admin_username',
               'admin_password', 'guest_status']
        self.__init__()
        for i, j in zip(data_user, key):
            self.write_data(i, j)
        if users is not None:
            self.update_users(users)

    def update_users(self, datas):
        key = ['username', 'password', 'paths', 'ftp_status', 'video_status', 'audio_status', 'pdf_status',
               'receive_status', 'send_status', 'system_control_status', 'picture_status', 'ftp_create_directory',
               'ftp_store_file', 'ftp_root']

        def _data(list_data) -> list:
            out = []
            for i in range(3, len(key)):
                try:
                    out.append(list_data[i])
                except IndexError:
                    out.append(None)
            return out

        for data in datas:
            data = list(data)
            try:
                self.new_user(data[1], data[2], data[3], _data(data[1:-1]), data[-1])
                continue
            except:
                pass
            for i, j in zip(data[1:], key):
                self.write_users_data(i, j, data[0])

    def user_data_by_username(self, username: str):
        return self.fetchone(f'SELECT * from users WHERE username = "{username}"')

    def user_data_by_id(self, user_id):
        return self.fetchone(f'SELECT * from users WHERE id = "{user_id}"')

    def write_users_data(self, data: str, data_type: str, user_id: int):
        self.sql_commit(f'UPDATE users SET {data_type} = "{data}" WHERE id = {user_id}')

    def new_user(self, username: str, password: str or None, paths: str, statuses: list, ftp_root):
        sql = f'INSERT INTO users (username, password, paths, ftp_status, video_status, audio_status, pdf_status, receive_status, send_status, system_control_status, picture_status, ftp_root) VALUES ("{username}", "{password}", "{paths}", "{statuses[0]}", "{statuses[1]}", "{statuses[2]}", "{statuses[3]}", "{statuses[4]}", "{statuses[5]}", "{statuses[6]}", "{statuses[7]}", "{ftp_root}")'
        self.sql_commit(sql)
        return self.user_data_by_username(username)

    def get_secret_data(self, secret: str):
        data = self.fetchone(f'SELECT * from secrets WHERE secret = "{secret}" AND status = "1"')
        # 24 hours later
        try:
            if data[2] > time.time() + 86400:
                self.disable_secret(data[0])
                return False
            return data
        except TypeError:
            return False

    def new_secret(self, username: str, link: str):
        # 24 hours later
        end_time = time.time() + 86400
        secret = random_token_url(32, 64)
        sql = f'INSERT INTO secrets (secret, link, time, username) VALUES ("{secret}", "{link}", {end_time}, "{username}")'
        self.sql_commit(sql)
        return secret

    def secret_check(self, username: str, link: str):
        return self.fetchone(f'SELECT * from secrets WHERE link = "{link}" AND username = "{username}" AND status = "1"')

    def disable_secret(self, secret: str):
        self.sql_commit(f'UPDATE secrets SET status = "0" WHERE secret = "{secret}"')

    def update_user_information(self, username, paths, ftp, video, audio, pdf, receive, send, system_control, picture, ftp_root):
        sql = f'UPDATE users SET paths = "{paths}", ftp_status = "{ftp}", video_status = "{video}", audio_status = "{audio}", pdf_status = "{pdf}", receive_status = "{receive}", send_status = "{send}", system_control_status = "{system_control}", picture_status = "{picture}", ftp_root = "{ftp_root}"  WHERE username = "{username}"'
        self.sql_commit(sql)

    def information_all_users(self):
        sql = 'SELECT username, ftp_status, video_status, audio_status, pdf_status,receive_status, send_status, system_control_status, picture_status from users'
        self.my_db.execute(sql)
        return self.my_db.fetchall()

    def ftp_users(self):
        sql = 'SELECT username, password, ftp_root  from users WHERE ftp_status = "1"'
        self.my_db.execute(sql)
        return self.my_db.fetchall()

    def get_all_users(self):
        sql = 'SELECT id, username from users'
        self.my_db.execute(sql)
        return self.my_db.fetchall()

database = Database()
