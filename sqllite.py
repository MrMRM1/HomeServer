import sqlite3


class Database:
    def __init__(self):
        self.data = sqlite3.connect('data.db')
        self.my_db = self.data.cursor()
        try:
            self.my_db.execute(f"SELECT * from data_user")
        except:
            self.my_db.execute("CREATE TABLE data_user (paths LONGTEXT NULL, port INT NULL, data_id CHAR(1) NULL)")

    def get_data(self):
        self.my_db.execute(f"SELECT * from data_user WHERE data_id = 1")
        return self.my_db.fetchone()

    def write_data(self, data, data_type):
        self.my_db.execute(f"SELECT * from data_user WHERE data_id = 1")
        if self.my_db.fetchone():
            sql = f'UPDATE data_user SET {data_type} = "{data}" WHERE data_id = 1'
        else:
            sql = f'INSERT INTO data_user ({data_type},data_id) VALUES ("{data}", 1)'
        self.my_db.execute(sql)
        self.data.commit()


