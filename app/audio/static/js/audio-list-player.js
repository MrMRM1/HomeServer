const jsmediatags = window.jsmediatags;
let len_audio = 0;
let audio_player = document.getElementById('player');
let audios = document.getElementsByClassName('audios');
let nameaudio = document.getElementById('nameaudio');
let auto_next_status = 1;
let btn_auto_next = document.getElementById('btn_auto_next');
let filename = '';

audio_name(0)
audio_player.src = audios[0].src;

function set_tags(index){
    jsmediatags.read(audios[index].src, {
        onSuccess: function(tag) {
            // Array buffer to base64
            const data = tag.tags.picture.data;
            const format = tag.tags.picture.format;
            let base64String = "";
            for (let i = 0; i < data.length; i++) {
                base64String += String.fromCharCode(data[i]);
            }
            // Output media tags
            navigator.mediaSession.metadata = new MediaMetadata({
                title : tag.tags.title,
                artist: tag.tags.artist,
                album: tag.tags.album,
                artwork : [
                        {
                            sizes: '512x512',
                            src: `data:${format};base64,${window.btoa(base64String)}`,
                            type: format
                        }
                    ]
            });
         },
        onError: function(error) {
            console.log(error);
        }
    });
}
function audio_name(a){
    let url = audios[a].src;
    filename = decodeURI(url.substring(url.lastIndexOf('/')+1));
    nameaudio.innerHTML = filename;
}

function next_audio(){
    if (len_audio == audios.length - 1){
        len_audio = 0;
    }
    else{
        len_audio = len_audio + 1;
    }
    play_audio(len_audio);


}

function back_audio(){
    if (len_audio == 0){
        len_audio = audios.length - 1;
    }
    else{
        len_audio = len_audio - 1;
    }
    play_audio(len_audio);
}

function play_audio(a){
    audio_name(a);
    audio_player.src = audios[a].src;
    audio_player.play();
    set_tags(a);
}

function auto_next(){
    if(auto_next_status == 1){
        auto_next_status = 0;
        btn_auto_next.value = "Auto Next Off";
    }
    else {
        auto_next_status = 1;
        btn_auto_next.value = "Auto Next On";
    }
}

audio_player.addEventListener('ended', function(){
    if (auto_next_status == 1){
        next_audio();
    }
});

if ( 'mediaSession' in navigator ) {
    set_tags(0);
    navigator.mediaSession.setActionHandler('pause', () => {
        audio_player.pause();
    });

    navigator.mediaSession.setActionHandler('play', () => {
        audio_player.play();
    });

    navigator.mediaSession.setActionHandler('seekbackward', (details) => {
        audio_player.currentTime = audio_player.currentTime - (details.seekOffset || 10);
    });

    navigator.mediaSession.setActionHandler('seekforward', (details) => {
        audio_player.currentTime = audio_player.currentTime + (details.seekOffset || 10);
    });

    navigator.mediaSession.setActionHandler('nexttrack', () => {
            next_audio();
        }
    );

    navigator.mediaSession.setActionHandler('previoustrack', () => {
            back_audio();
        }
    );
}