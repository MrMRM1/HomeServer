import os
import re
from sqllite import Database
from hashlib import md5
from threading import Thread
from time import sleep
from filename import pathfile
import platform

from flask import Flask, render_template, send_from_directory, request, redirect, make_response, jsonify

app = Flask(__name__)


def list_file(format_file, path):
    """
    :param format_file: The desired file format, for example mp4
    :param path: The desired folder path
    :return: Returns a list of files related to the imported format
    """
    files = []
    for i in format_file:
        for name in os.listdir(path):
            if re.match(rf'.*\.{i}', name):
                files.append(os.path.join(path, name))
    return files


def list_folders(path):
    """
    :param path: The desired folder path
    :return: Returns a list of all the folders in the path
    """
    return [x[0] for x in os.walk(path)]


def list_dir():
    """
    :return: Returns the list of folders stored in the database
    """
    database = Database()
    dirc = eval(database.get_data()[0])
    return dirc


def check_dir(path):
    """
    Check if the file is available through the page
    :param path: The requested file path on the page
    :return: Returns true if the file path is in the database, otherwise false
    """
    dircs = list_dir()
    status = False
    if '.' in path:
        path = path.split('/')
        del path[-1]
        path = "/".join(path)
    if path in dircs:
        status = True
    return status


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
        data = md5(data.encode()).hexdigest()
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


@app.route('/<path:link>')
def controls(link):
    temp_link = link.split('/')
    path = '/'.join(temp_link[1:])
    if link in ['video', 'pdf', 'audio', 'all_file']:
        return render_template("list_folders.html", title="List Folders", items=list_dir(), typs=link)
    elif check_dir(path):
        if temp_link[0] == 'video':
            return render_template("list_videos.html", title=path, items=list_file(['mkv', 'mp4'], path),
                                   typs="show_video")
        elif temp_link[0] == 'audio':
            return render_template("list_audios.html", title=path, items=list_file(['mp3'], path),
                                   typs="show_audio")
        elif temp_link[0] == 'pdf':
            return render_template("list_folders.html", title=path, items=list_file(['pdf'], path),
                                   typs="show_pdf")
        elif temp_link[0] == 'all_file':
            return render_template("list_folders.html", title=path, items=list_file(['*'], path),
                                   typs="dl_file")
        elif temp_link[0] == 'show_video':
            return render_template('video.html', title=path.split('/')[-1], link=path)
        elif temp_link[0] == 'show_audio':
            return render_template('list_audios.html', title=path.split('/')[-1], link=path)
        elif temp_link[0] == 'show_pdf':
            return render_template('viewer.html', title=path.split('/')[-1], link=path)
    else:
        return redirect('/', code=302)


@app.route('/file/<path:filename>')
def download_file(filename):
    if os.name != 'nt':
        filename = '/' + filename
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
