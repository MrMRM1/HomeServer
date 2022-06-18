import sqlite3
from pathlib import Path
from os.path import join as join_path
from scripts.network import port_flask

path_received = join_path(Path.home().__str__(), 'Downloads', 'HomeServerReceived')


class Database:
    def __init__(self):
        self.data = sqlite3.connect('data.db')
        self.my_db = self.data.cursor()
        try:
            self.my_db.execute(f"SELECT * from data_user")
        except:
            self.my_db.execute(f'CREATE TABLE data_user (paths LONGTEXT NULL, port INT DEFAULT {port_flask()}, data_id DEFAULT 1 ,upload DEFAULT "{path_received}", password TEXT NULL)')
            sql = f'INSERT INTO data_user (data_id) VALUES (1)'
            self.my_db.execute(sql)
            self.data.commit()

    def get_data(self):
        self.my_db.execute(f"SELECT * from data_user WHERE data_id = 1")
        return self.my_db.fetchone()

    def write_data(self, data, data_type):
        sql = f'UPDATE data_user SET {data_type} = "{data}" WHERE data_id = 1'
        self.my_db.execute(sql)
        self.data.commit()


