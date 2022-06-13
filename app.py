import os
from libraries.sqllite import Database
from hashlib import sha256
from threading import Thread
from time import sleep
from libraries.filename import pathfile
import platform
from video import video
from audio import audio
from pdf import pdf
from picture import picture
from libraries.paths import check_dir, list_dir, list_file, edit_path_windows_other

from flask import Flask, render_template, send_from_directory, request, redirect, make_response, jsonify

app = Flask(__name__)
app.secret_key = "add your secret key"

app.register_blueprint(video)
app.register_blueprint(audio)
app.register_blueprint(pdf)
app.register_blueprint(picture)


def shutdown_sleep_thread(value):
    """
    :param value: Sleep or Shutdown
    :return: Delayed shutdown or sleep mode after 3 seconds
    """
    sleep(3)
    if value == "Sleep":
        match platform.system():
            case 'Windows':
                os.system("rundll32.exe powrprof.dll, SetSuspendState Sleep 2")
            case 'Darwin':
                os.system("pmset sleepnow")
            case _:
                os.system("systemctl suspend")
    elif value == "Shutdown":
        if platform.system() == 'Windows':
            os.system("shutdown /s /t 2")
        else:
            os.system("shutdown -h now")


@app.route('/')
def home_page():
    return render_template("home.html", title="Home")


@app.route('/system_control', methods=['POST'])
def check_password_system_page():
    data = request.form['password']
    database = Database()
    password = database.get_data()[4]
    alert = None
    if data != '':
        data = sha256(data.encode()).hexdigest()
        if data == password:
            if 'Sleep' in request.form:
                sleep_thread = Thread(target=shutdown_sleep_thread, args=('Sleep',))
                sleep_thread.start()
                alert = 'The Sleep was successful'
            elif 'Shutdown' in request.form:
                shutdown_thread = Thread(target=shutdown_sleep_thread, args=('Shutdown',))
                shutdown_thread.start()
                alert = 'The shutdown was successful'
        else:
            alert = 'Password incorrect'
    elif data == '':
        alert = 'Fill in the password field'
    return render_template("systemcontroll.html", title="System control", alert=alert)


@app.route('/system_control', methods=['GET'])
def system_page():
    return render_template("systemcontroll.html", title="System Control")


@app.route('/all_file')
def all_file_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='all_file')


@app.route('/all_file/<path:link>')
def controls(link):
    if check_dir(link):
        return render_template("list_folders.html", title=link, items=list_file(['*'], link), typs="dl_file")
    else:
        return redirect('/all_file')


@app.route('/file/<path:filename>')
def download_file(filename):
    filename = edit_path_windows_other(filename)
    if check_dir(filename):
        rt = filename.split('/')
        name = rt[-1]
        del rt[-1]
        return send_from_directory('/'.join(rt), name)
    else:
        return redirect('/', code=302)


@app.route('/upload', methods=['GET'])
def uploads_file():
    return render_template('send.html', title="Send")


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        database = Database()
        path = database.get_data()[3]
        try:
            f.save(pathfile(path, f.filename))
        except:
            os.makedirs(f"{path}")
            f.save(pathfile(path, f.filename))
        res = make_response(jsonify({"message": "File uploaded"}), 200)

        return res
    return render_template('send.html', title="Send")
