from pathlib import Path

from app.scripts.paths import *


def test_edit_path_windows_other():
    if os.name == 'nt':
        assert edit_path_windows_other('C://Users/Default User/') == 'C://Users/Default User/'
        assert edit_path_windows_other('C://Users/Default User/') != '/C://Users/Default User/'
    else:
        assert edit_path_windows_other('Users/Default User/') == '/Users/Default User/'
        assert edit_path_windows_other('Users/Default User/') != 'Users/Default User/'


def test_list_file():
    for i in list_file(['py'], os.path.dirname(__file__)):
        assert os.path.splitext(i)[1] == '.py'
    for i in list_file(['mp3'], os.path.dirname(__file__)):
        assert os.path.splitext(i)[1] != '.py'


def test_list_dir():
    path_received = os.path.join(Path.home().__str__(), 'Downloads', 'HomeServer')
    assert len(list_dir()) == 1
    assert list_dir()[0] == path_received


def test_check_dir_flask():
    @check_dir_flask
    def route_test(link):
        return True

    path_received = os.path.join(Path.home().__str__(), 'Downloads', 'HomeServer')

    assert route_test(path_received) is True
    assert route_test('/Users/Download') is not True
