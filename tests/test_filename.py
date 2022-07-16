import os

from app.scripts.filename import pathfile


def test_pathfile():
    new_file = pathfile('.', 'test_filename.py')
    assert new_file == './test_filename(1).py'
    open(new_file, 'w').close()
    assert pathfile('.', 'test_filename(1).py') != new_file
    assert pathfile('.', 'test_filename(1).py') == './test_filename(2).py'
    os.remove(new_file)
