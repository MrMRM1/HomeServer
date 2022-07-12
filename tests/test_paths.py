from app.scripts.paths import *
import os


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
