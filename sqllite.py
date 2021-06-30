import sqlite3


class Database:
    def __init__(self):
        self.data = sqlite3.connect('data.db')
        self.my_db = self.data.cursor()
        try:
            self.my_db.execute(f"SELECT * from paths")
        except:
            self.my_db.execute("CREATE TABLE paths (paths LONGTEXT NULL, data_id CHAR(1) NULL)")

    def get_data(self):
        self.my_db.execute(f"SELECT * from paths WHERE data_id = 1")
        return self.my_db.fetchone()

    def write_data(self, paths):
        self.my_db.execute(f"SELECT * from paths WHERE data_id = 1")
        if self.my_db.fetchone():
            sql = f'UPDATE paths SET paths = "{paths}" WHERE data_id = 1'
        else:
            sql = f'INSERT INTO paths (paths,data_id) VALUES ("{paths}", 1)'
        self.my_db.execute(sql)
        self.data.commit()

