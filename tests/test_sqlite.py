from pathlib import Path
import os

from app.scripts.sqllite import Database
from app.scripts.network import port_flask


def test_init():
    if 'data.db' in os.listdir(os.path.dirname(__file__)):
        os.remove('data.db')
    database = Database()
    assert 'data.db' in os.listdir(os.path.dirname(__file__))


def test_get_data():
    database = Database()
    path_received = os.path.join(Path.home().__str__(), 'Downloads', 'HomeServerReceived')
    default_data = [None, int(port_flask()), "1", path_received, None, 8821, "0", None, "0", "0", "0"]
    for i, j in zip(database.get_data(), default_data):
        assert i == j


def test_write_data():
    database = Database()
    path_received = os.path.join(Path.home().__str__(), 'Downloads', 'HomeServer')
    data = {'paths': path_received, 'port': 8888, 'data_id': "1", 'upload': path_received,
            'password': '1s3M4a5', 'port_ftp': 8822, 'ftp_server': '1', 'ftp_root': path_received,
            'ftp_create_directory': '0', 'ftp_store_file': '1', 'run_background': '1'}
    for i in data.keys():
        database.write_data(data[i], i)
    new_data = database.get_data()
    for i, j in zip(new_data, data.values()):
        assert i == j
