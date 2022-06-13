from . import pdf
from libraries.paths import list_dir, list_file, check_dir

from flask import render_template, redirect


@pdf.route('/pdf')
def list_folders():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='pdf')


@pdf.route('/pdf/<path:link>')
def list_pdf(link):
    if check_dir(link):
        return render_template("list_folders.html", title=link, items=list_file(['pdf'], link), typs="show_pdf")
    else:
        return redirect('/pdf')


@pdf.route('/show_pdf/<path:link>')
def show_pdf(link):
    if check_dir(link):
        return render_template('viewer.html', title=link.split('/')[-1], link=link)
    else:
        return redirect('/pdf')
