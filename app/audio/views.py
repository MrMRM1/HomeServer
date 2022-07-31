from flask import render_template

from . import audio
from app.scripts.paths import list_dir, list_file, check_dir_flask
from app.admin.scripts.login import login_required_custom, access_status


@audio.route('/audio')
@login_required_custom
def audio_page():
    if access_status(6):
        return render_template("list_folders.html", title="List Folders", items=','.join(list_dir()), typs="audio")


@audio.route('/audio/<path:link>')
@login_required_custom
@check_dir_flask
def list_audios(link):
    if access_status(6):
        return render_template("list_audios.html", title=link, items=list_file(['mp3', 'wav', 'ogg'], link),
                               typs="show_audio")
