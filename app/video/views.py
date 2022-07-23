import json
import time

from flask import render_template, request, jsonify
from flask_login import current_user

from . import video
from app.scripts.paths import list_dir, list_file, check_dir_flask, check_path
from app.admin.scripts.login import login_required_custom, access_status
from app.scripts.sqllite import database


@video.route('/video')
@login_required_custom
def video_page():
    if access_status(5):
        return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='video')


@video.route('/video/<path:link>')
@login_required_custom
@check_dir_flask
def list_videos(link):
    if access_status(5):
        return render_template("list_videos.html", title=link,
                               items=list_file(['avi', 'mpg', 'mpe', 'mpeg', 'asf', 'wmv', 'mov', 'qt', 'rm', 'mp4',
                                                'flv', 'm4v', 'webm', 'ogv', 'ogg', 'mkv', 'ts', 'tsv'], link),
                               typs="show_video")


@video.route('/show_video/<path:link>', methods=['GET'])
@login_required_custom
@check_dir_flask
def show_video(link):
    if access_status(5):
        return render_template('video.html', title=link.split('/')[-1], link=link)


@video.route('/show_video', methods=['POST'])
@login_required_custom
def creat_secret():
    data = json.loads(request.data)
    link = data['link'].partition('file/')[2]
    username = current_user.username
    if check_path(link):
        old_secret = database.secret_check(username, link)
        if old_secret is not None:
            # 2 hours later
            if old_secret[2] > time.time() + 79200:
                secret = old_secret[0]
            else:
                database.disable_secret(old_secret[0])
                secret = database.new_secret(link, username)
        else:
            secret = database.new_secret(link, username)
        return jsonify(status=200, url=request.headers['Origin']+'/file/'+link+'?secret='+secret), 200
    else:
        return jsonify(status=403, text='Access is not allowed'), 200

