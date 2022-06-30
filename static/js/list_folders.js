var typs = $('#typs').html()
var download = ''

if (typs === 'dl_file'){
    download = 'download'
}

var root = ''
var location_dir = 0
if (root != ''){
    location_dir = root.split('/').length + 1
}
const color = ['btn-primary', 'btn-success', 'btn-danger', 'btn-warning', 'btn-info']
var test = $('#data').html()
var datas = test.split(',')
function cwd(data, location_dir){
    var dirs = []
    for (var i in data){
        temp = data[i].split('/')
        var name = temp[0]
        if (location_dir > 0){
            for (var j=1; j < location_dir; j++){

                if (temp[j] != undefined){
                    name += '/' + temp[j]
                }
                else{
                    break;
                }
            }
        }
        if ((!dirs.includes(name)) && (name.includes(root))){
            dirs.push(name)
        }
    }
    return dirs
}

function replace_me(text, a, b){
    text = text.split(a)
    return text.join(b)
}

function click_btn(elmt){
    if (elmt == 'Open%20the%20folder'){
        url = '/' + typs + '/' + root
        url = url.split('/')
        url.pop(url.length - 1)
        window.location = url.join('/')
    }
    else
    {
        if (location_dir == 0){
            location_dir += 2
        }
        else {
            location_dir += 1
        }

        root +=  replace_me(elmt, '%20', ' ')
        dirs = []
        if (datas.includes(root)){
            dirs.push('/Open the folder')
        }
        root += '/'

        dirs = dirs.concat(cwd(datas, location_dir))
        if (dirs.length == 1){
            if (dirs[0] != '/Open the folder'){
                path = dirs[0].split('/')
                click_btn(path[path.length - 1])
            }
            else{
                creator(dirs)
            }
        }
        else{
            creator(dirs)
        }


    }

}

function show_name(elmt){
    a = elmt.split('/')
    return a[a.length - 1 ]
}


function creator(dirs, download=''){
    function text_make (i){
        return '<a class="btn ' + color[i % 5] + ' m-2 p-3 rounded-3 col-md-6 d-flex justify-content-between" ' + download +' onclick=click_btn("'+ replace_me(show_name(dirs[i])," ", "%20")+'")><h1 class="mt-auto mb-auto text-break">' + show_name(dirs[i]) + '</h1></a>'
    }
    var lengh_dir = dirs.length
    $('#list').remove()
    $('#path').html(root)
    if (lengh_dir != 0){
        $('#main').append('<div id="list" class="col-8 mt-2 ms-auto me-auto"></div>')
        for (let i=0; i < lengh_dir; i = i+2){
            $('#list').append('<div id="group'+ i +'" class="d-md-flex ms-auto me-auto justify-content-md-around"></div>')
            if (i != lengh_dir){
                $('#group' + i).append(text_make(i))
            }
            if (((i+1) / lengh_dir) != 1){
                $('#group' + i).append(text_make(i+1))
            }

        }

    }
}
dirs = cwd(datas, location_dir)
creator(dirs)
