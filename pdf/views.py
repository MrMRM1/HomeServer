from . import pdf
from scripts.paths import list_dir, list_file, check_dir_flask

from flask import render_template


@pdf.route('/pdf')
def list_folders():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='pdf')


@pdf.route('/pdf/<path:link>')
@check_dir_flask
def list_pdf(link):
    return render_template("list_folders.html", title=link, items=list_file(['pdf'], link), typs="show_pdf")


@pdf.route('/show_pdf/<path:link>')
@check_dir_flask
def show_pdf(link):
    return render_template('viewer.html', title=link.split('/')[-1], link=link)
