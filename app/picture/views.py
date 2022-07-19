from flask import render_template

from . import picture
from scripts.paths import list_dir, list_file, check_dir_flask


@picture.route('/picture')
def list_folders():
    return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='picture')


@picture.route('/picture/<path:link>')
@check_dir_flask
def picture_page(link):
    return render_template("picture.html", title=link,
                           items=list_file(['apng', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp',
                                            'png', 'png'], link), typs="show_picture")