from . import audio
from libraries.paths import list_dir, list_file, check_dir

from flask import render_template, redirect


@audio.route('/audio')
def audio_page():
    return render_template("list_folders.html", title="List Folders", items=list_dir(), typs="audio")


@audio.route('/audio/<path:link>')
def list_audios(link):
    if check_dir(link):
        return render_template("list_audios.html", title=link, items=list_file(['mp3', 'wav', 'ogg'], link),
                               typs="show_audio")
    else:
        return redirect('/audio')
