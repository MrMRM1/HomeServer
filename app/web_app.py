import os
from hashlib import sha256
from threading import Thread

from flask import Flask, render_template, send_from_directory, request, make_response, jsonify, redirect
from flask_login import LoginManager, current_user, logout_user

from scripts.sqllite import database
from scripts.filename import pathfile
from video import video
from audio import audio
from pdf import pdf
from picture import picture
from admin import admin
from scripts.paths import check_dir_flask, list_dir, list_file, edit_path_windows_other
from scripts.system_control import shutdown_sleep_thread
from admin.scripts.user import User
from admin.scripts.login import user_login, error_login, login_required_custom, access_status

app = Flask(__name__)
app.secret_key = "add your secret key"

app.register_blueprint(video)
app.register_blueprint(audio)
app.register_blueprint(pdf)
app.register_blueprint(picture)
app.register_blueprint(admin)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/login', methods=['GET'])
def login():
    try:
        _ = current_user.username
        return redirect('/')
    except AttributeError:
        guest = False
        if database.get_data()[14] == '1':
            guest = True
        return render_template('login.html', guest=guest)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/login', methods=['POST'])
def login_post():
    data = database.get_data()
    if 'sing_in' in request.form:

        username = request.form['username_home']
        password = sha256(request.form['password'].encode()).hexdigest()

        if username == '' or password == '':
            return error_login(data[14])

        # admin user
        if username == data[12]:
            if data[13] == password:
                return user_login(username)
            else:
                return error_login(data[14])
        # Other users
        else:
            user_data = database.user_data_by_username(username)
            if user_data is not None and password == user_data[2]:
                return user_login(username)
            else:
                return error_login(data[14])

    elif 'guest' in request.form and data[14] == '1':
        return user_login('guest')


@login_manager.user_loader
def load_user(username):
    if database.user_data_by_username(username) or database.get_data()[12] == username:
        return User(username)


@app.route('/')
@login_required_custom
def home_page():
    data = database.get_data()
    if data[11] == '1':
        username = current_user.username
        if username == data[12]:
            return render_template("home.html", title="Home", login_status=False)
        else:
            user_data = ','.join(database.user_data_by_username(username)[5:12])
            return render_template("home.html", title="Home", login_status=True, data=user_data)
    else:
        return render_template("home.html", title="Home", login_status=False)


@app.route('/system_control', methods=['POST'])
@login_required_custom
def check_password_system_page():
    if access_status(10):
        data = request.form['password']
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
@login_required_custom
def system_page():
    if access_status(10):
        return render_template("systemcontroll.html", title="System Control")


@app.route('/all_file')
@login_required_custom
def all_file_page():
    if access_status(8):
        return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='all_file')


@app.route('/all_file/<path:link>')
@login_required_custom
@check_dir_flask
def controls(link):
    if access_status(8):
        return render_template("list_folders.html", title=link, items=','.join(list_file(['*'], link)), typs="dl_file")


@app.route('/file/<path:link>')
@login_required_custom
@check_dir_flask
def download_file(filename):
    filename = edit_path_windows_other(filename)
    rt = filename.split('/')
    name = rt[-1]
    del rt[-1]
    return send_from_directory('/'.join(rt), name)


@app.route('/send', methods=['GET'])
@login_required_custom
def uploads_file():
    if access_status(9):
        return render_template('send.html', title="Send")


@app.route('/send', methods=['POST'])
@login_required_custom
def upload_file():
    if access_status(9):
        if request.method == 'POST':
            f = request.files['file']
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
