let len_audio = 0;
let audio_player = document.getElementById('player');
let audios = document.getElementsByClassName('audios');
let nameaudio = document.getElementById('nameaudio');
let auto_next_status = 1;
let btn_auto_next = document.getElementById('btn_auto_next');
audio_name(0)
audio_player.src = audios[0].src;

function audio_name(a){
    var url = audios[a].src;
    var filename = url.substring(url.lastIndexOf('/')+1);
    nameaudio.innerHTML = decodeURI(filename)
}

function next_audio(){
    if (len_audio == audios.length - 1){
        len_audio = 0;
    }
    else{
        len_audio = len_audio + 1;
    }
    audio_name(len_audio)
    audio_player.src = audios[len_audio].src;
    audio_player.play();
}

function back_audio(){
    if (len_audio == 0){
        len_audio = audios.length - 1;
    }
    else{
        len_audio = len_audio - 1;
    }
    audio_name(len_audio)
    audio_player.src = audios[len_audio].src;
    audio_player.play();
}

function play_audio(a){
    len_audio = a;
    audio_name(a);
    audio_player.src = audios[a].src;
    audio_player.play();
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