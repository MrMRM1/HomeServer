from flask import Flask, render_template, send_from_directory, request, redirect, make_response, jsonify
import os
import re
from sqllite import Database
from hashlib import md5

app = Flask(__name__)


def list_file(format, path):
    fils = []
    for i in format:
        for name in os.listdir(path):
            if re.match(rf'.*\.{i}', name):
                fils.append(os.path.join(path, name))
    return fils


def list_folders(path):
    return [x[0] for x in os.walk(path)]


def list_dir():
    database = Database()
    dirc = eval(database.get_data()[0])
    return dirc


def check_dir(path):
    dircs = list_dir()
    status = False
    if '.' in path:
        path = path.split('/')
        del path[-1]
        path = "/".join(path)
    if path in dircs:
        status = True
    return status


@app.route('/')
def home_page():
    return render_template("home.html", title="Home")


@app.route('/system_PC', methods=['POST'])
def check_password_system_page():
    data = request.form['password']
    database = Database()
    password = database.get_data()[4]
    alert = None
    if data is not None:
        data = md5(data.encode()).hexdigest()
        if data == password:
            try:
                btn = request.form['Sleep']
                os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep 2")
                alert = 'Sleep PC'
            except:
                btn = request.form['Shutdown']
                os.system("shutdown /s /t 2")
                alert = 'Shutdown PC'
        else:
            alert = 'Password incorrect'
    elif data is None:
        alert = 'Fill in the password field'
    return render_template("systemcontroll.html", title="System control", alert=alert)


@app.route('/system_PC', methods=['GET'])
def system_page():
    return render_template("systemcontroll.html", title="System Control")


@app.route('/<path:link>')
def controls(link):
    check_path = re.search(r".:\/", link)
    if link in ['video', 'pdf', 'audio', 'all_file']:
        typs = link
        return render_template("list_folders.html", title="List Folders", items=list_dir(), typs=typs)
    elif check_path and check_dir(link[check_path.span()[0]:]):
        if link[:5] == 'video':
            return render_template("list_videos.html", title=link[6:], items=list_file(['mkv', 'mp4'], link[6:]),
                                   typs="show_video")
        elif link[:5] == 'audio':
            return render_template("list_audios.html", title=link[6:], items=list_file(['mp3'], link[6:]),
                                   typs="show_audio")
        elif link[:3] == 'pdf':
            return render_template("list_folders.html", title=link[4:], items=list_file(['pdf'], link[4:]),
                                   typs="show_pdf")
        elif link[:8] == 'all_file':
            return render_template("list_folders.html", title=link[9:], items=list_file(['*'], link[9:]),
                                   typs="dl_file")
        elif link[:10] == 'show_video':
            return render_template('video.html', title=link.split('/')[-1], link=link[11:])
        elif link[:10] == 'show_audio':
            return render_template('list_audios.html', title=link.split('/')[-1], link=link[11:])
        elif link[:8] == 'show_pdf':
            return render_template('viewer.html', title=link.split('/')[-1], link=link[9:])
    else:
        return redirect('/', code=302)


@app.route('/file/<path:filename>')
def download_file(filename):
    check_path = re.search(r".:\/", filename)
    if check_path and check_dir(filename[check_path.span()[0]:]):
        rt = filename.split('/')
        name = rt[-1]
        del rt[-1]
        return send_from_directory('/'.join(rt), name)
    else:
        redirect('/', code=302)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'The program was stopped.'


@app.route('/upload', methods=['GET'])
def uploads_file():
    return render_template('upload.html', title="Upload")


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        database = Database()
        path = database.get_data()[3]
        try:
            f.save(f'{path}/{f.filename}')
        except:
            os.makedirs(f"{path}")
            f.save(f'{path}/{f.filename}')
        res = make_response(jsonify({"message": "File uploaded"}), 200)

        return res
    return render_template('upload.html', title="Upload")

