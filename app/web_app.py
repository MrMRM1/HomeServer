import os
from hashlib import sha256
from threading import Thread

from flask import Flask, render_template, send_from_directory, request, make_response, jsonify
from flask_login import LoginManager

from scripts.sqllite import Database, database
from scripts.filename import pathfile
from video import video
from audio import audio
from pdf import pdf
from picture import picture
from scripts.paths import check_dir_flask, list_dir, list_file, edit_path_windows_other
from scripts.system_control import shutdown_sleep_thread
from admin.scripts.user import User

app = Flask(__name__)
app.secret_key = "add your secret key"

app.register_blueprint(video)
app.register_blueprint(audio)
app.register_blueprint(pdf)
app.register_blueprint(picture)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/login', methods=['GET'])
def login():
    guest = False
    if database.get_data()[13] == '1':
        guest = True
    return render_template('login.html', guest=guest)


@login_manager.user_loader
def load_user(username):
    if database.get_user_data(username) or database.get_data()[12] == username:
        return User(username)


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
    return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='all_file')


@app.route('/all_file/<path:link>')
@check_dir_flask
def controls(link):
    return render_template("list_folders.html", title=link, items=','.join(list_file(['*'], link)), typs="dl_file")


@app.route('/file/<path:link>')
@check_dir_flask
def download_file(filename):
    filename = edit_path_windows_other(filename)
    rt = filename.split('/')
    name = rt[-1]
    del rt[-1]
    return send_from_directory('/'.join(rt), name)


@app.route('/send', methods=['GET'])
def uploads_file():
    return render_template('send.html', title="Send")


@app.route('/send', methods=['POST'])
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


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
