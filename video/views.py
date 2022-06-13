from . import video
from libraries.paths import list_dir, list_file

from flask import render_template


@video.route('/video')
def video_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs='video')


@video.route('/video/<path:link>')
def controls(link):
    return render_template("list_videos.html", title=link, items=list_file(['mkv', 'mp4'], link), typs="show_video")


@video.route('/show_video/<path:link>')
def show_video(link):
    return render_template('video.html', title=link.split('/')[-1], link=link)