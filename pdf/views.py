from . import pdf
from libraries.paths import list_dir, list_file

from flask import render_template


@pdf.route('/pdf')
def video_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='pdf')


@pdf.route('/pdf/<path:link>')
def controls(link):
    return render_template("list_folders.html", title=link, items=list_file(['pdf'], link), typs="show_pdf")


@pdf.route('/show_pdf/<path:link>')
def show_video(link):
    return render_template('viewer.html', title=link.split('/')[-1], link=link)