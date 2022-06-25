from flask import render_template

from . import audio
from scripts.paths import list_dir, list_file, check_dir_flask


@audio.route('/audio')
def audio_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs="audio")


@audio.route('/audio/<path:link>')
@check_dir_flask
def list_audios(link):
    return render_template("list_audios.html", title=link, items=list_file(['mp3', 'wav', 'ogg'], link),
                           typs="show_audio")
