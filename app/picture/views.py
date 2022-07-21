from flask import render_template

from . import picture
from scripts.paths import list_dir, list_file, check_dir_flask
from app.admin.scripts.login import login_required_custom, access_status


@picture.route('/picture')
@login_required_custom
def list_folders():
    if access_status(11):
        return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='picture')


@picture.route('/picture/<path:link>')
@login_required_custom
@check_dir_flask
def picture_page(link):
    if access_status(11):
        return render_template("picture.html", title=link,
                               items=list_file(['apng', 'gif', 'ico', 'cur', 'jpg', 'jpeg', 'jfif', 'pjpeg', 'pjp',
                                                'png', 'png'], link), typs="show_picture")
