from flask import render_template

from . import pdf
from scripts.paths import list_dir, list_file, check_dir_flask
from app.admin.scripts.login import login_required_custom, access_status


@pdf.route('/pdf')
@login_required_custom
def list_folders():
    if access_status(7):
        return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='pdf')


@pdf.route('/pdf/<path:link>')
@login_required_custom
@check_dir_flask
def list_pdf(link):
    if access_status(7):
        return render_template("list_folders.html", title=link, items=list_file(['pdf'], link), typs="show_pdf")


@pdf.route('/show_pdf/<path:link>')
@login_required_custom
@check_dir_flask
def show_pdf(link):
    if access_status(7):
        return render_template('viewer.html', title=link.split('/')[-1], link=link)
