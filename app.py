from flask import Flask, render_template, send_from_directory
import os
import re
from sqllite import Database
database = Database()
dirctory = eval(database.get_data()[0])
app = Flask(__name__)


def list_file(format, path):
    fils = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:

                if re.match(rf'.*\.{format}', name):
                    fils.append(os.path.join(root, name))

    return fils

@app.route('/')
def home_page():
    return render_template("home.html", title="Home")




@app.route('/<path:link>')
def controls(link):
    print(link)
    if link in ['video', 'pdf', 'audio']:
        typs = link
        return render_template("list_files.html", title="Folder list", items=dirctory, typs=typs)
    elif link[:5] == 'video':
        return render_template("list_files.html", title=link[6:], items=list_file('mp4', link[6:]), typs="show_video")
    elif link[:5] == 'audio':
        return render_template("list_files.html", title=link[6:], items=list_file('mp3', link[6:]), typs="show_audio")
    elif link[:3] == 'pdf':
        return render_template("list_files.html", title=link[4:], items=list_file('pdf', link[4:]), typs="show_pdf")
    elif link[:10] == 'show_video':
        return render_template('video.html', title=link.split('/')[-1], link=link[11:])
    elif link[:10] == 'show_audio':
        return render_template('audio.html', title=link.split('/')[-1], link=link[11:])
    elif link[:8] == 'show_pdf':
        return render_template('viewer.html', title=link.split('/')[-1], link=link[9:])


@app.route('/file/<path:filename>')
def download_file(filename):
    rt = filename.split('/')
    name = rt[-1]
    del rt[-1]
    return send_from_directory('/'.join(rt), name)



