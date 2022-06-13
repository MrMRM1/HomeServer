from . import picture
from libraries.paths import list_dir, list_file, check_dir

from flask import render_template, redirect


@picture.route('/picture')
def picture_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='picture')


@picture.route('/picture/<path:link>')
def controls(link):
    if check_dir(link):
        return render_template("picture.html", title=link,
                               items=list_file(['apng', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp',
                                                'png', 'png'], link), typs="show_picture")
    else:
        return redirect('/picture')
