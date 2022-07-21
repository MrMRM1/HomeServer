from flask import render_template, abort

from . import video
from app.scripts.paths import list_dir, list_file, check_dir_flask
from app.admin.scripts.login import login_required_custom, access_status


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


@video.route('/show_video/<path:link>')
@login_required_custom
@check_dir_flask
def show_video(link):
    if access_status(5):
        return render_template('video.html', title=link.split('/')[-1], link=link)
