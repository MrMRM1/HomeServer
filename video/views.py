from . import video
from scripts.paths import list_dir, list_file, check_dir_flask

from flask import render_template


@video.route('/video')
def video_page():
    return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs='video')


@video.route('/video/<path:link>')
@check_dir_flask
def list_videos(link):
    return render_template("list_videos.html", title=link,
                           items=list_file(['avi', 'mpg', 'mpe', 'mpeg', 'asf', 'wmv', 'mov', 'qt', 'rm', 'mp4',
                                            'flv', 'm4v', 'webm', 'ogv', 'ogg', 'mkv', 'ts', 'tsv'], link),
                           typs="show_video")


@video.route('/show_video/<path:link>')
@check_dir_flask
def show_video(link):
    return render_template('video.html', title=link.split('/')[-1], link=link)
