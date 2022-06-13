from . import picture
from libraries.paths import list_dir, list_file

from flask import render_template


@picture.route('/picture')
def picture_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='picture')


@picture.route('/picture/<path:link>')
def controls(link):
    return render_template("picture.html", title=link,
                            items=list_file(['apng', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg',
                                            'pjp', 'png', 'png'], link), typs="show_picture")


@picture.route('/show_picture/<path:link>')
def show_picture(link):
    return render_template('video.html', title=link.split('/')[-1], link=link)