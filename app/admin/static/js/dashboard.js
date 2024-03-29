let username = [];
let paths = [];
const password_pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/gm;
const username_pattern = /^(?=.{4,20}$)[a-zA-Z0-9]+$/gm;
let close_menu = document.getElementById('close_menu');

// functions 

function get_root_ftp(path, advance){
    let roots = []
    
    function append_root(index){
        for (let i in path){
            let path_split = path[i].split('/')
            let temp = [];
            for (let j=0; j<index; j++){
                let folder = path_split[j]
                if (!temp.includes(folder)){
                    temp.push( folder ) 
                }
            }
            let root =  temp.join('/') + '/'   
            if ( !roots.includes(root) ) {
                roots.push(root)
            } 
        }
    }
    for (let i=1; i < advance+1; i++){
        append_root(i)
    }
    
    return roots
}

function remove_valid_invalid(element){
    element.classList.remove('is-invalid');
    element.classList.remove('is-valid');
}

function post_data(url, data){
    return fetch(url, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
    }).then(response => response.json()).then(jsonObject => {
        return jsonObject
    });
}

function my_alert(element, message, typeAlert){
    document.getElementById(element).innerHTML = `<div class="alert ${typeAlert}">${message}</div>`;
        setTimeout(function(){
            document.getElementById(element).innerHTML = '';
        }, 6000);
}

function showAlert(message, typeAlert){
    my_alert('myAlert', message, typeAlert);
}

function new_user_showAlert(message, typeAlert){
    my_alert('new_user_myAlert', message, typeAlert)
}

function update_access_showAlert(message, typeAlert){
    my_alert('update_access_myAlert', message, typeAlert)
}

function settings_showAlert(message, typeAlert){
    my_alert('settings_myAlert', message, typeAlert)
}

function _checkbox(status){
    if (status == '1'){
        return '<td><input type="checkbox" disabled checked></td>'
    }
    return '<td><input type="checkbox" disabled></td>'
}

function valid_and_invalid(element, condition){
    remove_valid_invalid(element);
    if (condition){
        element.classList.add('is-valid');
        return true
    }
    else {
        element.classList.add('is-invalid');
        return false
    }
    
}

function check_input_select(element){
    return valid_and_invalid(element, element.value !== 'Choose...');
}

function check_username(element){
    return valid_and_invalid(element, element.value.match(username_pattern));
}

function check_password(element){
    return valid_and_invalid(element, element.value.match(password_pattern));
}

function check_password_verification(password, password_v){
    return valid_and_invalid(password_v, (password.value == password_v.value) && (password_v.value.match(password_pattern)));
}

function check_username_select(element){
    return valid_and_invalid(element, username.includes(element.value));
}

function get_paths_user(idcheckbox, idlabel){
    let paths_user = [];
    for (let i in paths){
        let check_box = document.getElementById(idcheckbox + i);
        let path = document.getElementById(idlabel + i);
        if (check_box.checked){
            paths_user.push(path.innerHTML);
        }
    }
    
    return paths_user
}

function checkbox_status(element){
    if (element.checked){
        return '1'
    }
    return '0'
}

function inner_username(element){
    for (let i in username){
        element.innerHTML += `<option value="${username[i]}">${username[i]}</option>`
    }
}

function set_checked(element, status){
    if (status == '1'){
        element.checked = true;
    }
    else {
        element.checked = false;
    }
}

function set_checkbox_status(data){
    set_checked(update_access_checkbox_audio, data.audio)
    set_checked(update_access_checkbox_ftp, data.ftp)
    set_checked(update_access_checkbox_receive, data.receive)
    set_checked(update_access_checkbox_video, data.video)
    set_checked(update_access_checkbox_send, data.send)
    set_checked(update_access_checkbox_system_control, data.system_control)
    set_checked(update_access_checkbox_pdf, data.pdf)
    set_checked(update_access_checkbox_picture, data.picture)
    set_checked(update_access_checkbox_create_directory, data.ftp_create_directory)
    set_checked(update_access_checkbox_store_file, data.ftp_store_file)
}

function set_checkbox_settings(data){
    set_checked(setting_checkbox_guest_mode, data.guest)
    set_checked(settings_checkbox_run_background, data.run_background)
    set_checked(settings_checkbox_ftp_create_directory, data.ftp_create_directory)
    set_checked(settings_checkbox_ftp_store_file, data.ftp_store_file)
    set_checked(setting_checkbox_ftp, data.ftp)
    set_checked(setting_checkbox_login, data.login)
}

function set_user_path(user_paths, ftp_root){
    update_access_paths.innerHTML = ''
    user_paths = user_paths.split(',')
    post_data('/admin/get_paths', {}).then(jsonObject => {
        paths = jsonObject.paths.split(',')
        for (let i in paths){
            let checked_status = '';
            if (user_paths.includes(paths[i])){
                checked_status = 'checked';
            }
            update_access_paths.innerHTML += `<div class="form-check ms-1"><input class="form-check-input" type="checkbox" value="" id="update_access_path_checkbox${i}" ${checked_status}><label class="form-check-label text-nowrap" for="update_access_path_checkbox${ i }" id="update_access_path_label${i}">${paths[i]}</label></div>`;
        }
        set_ftp_root(ftp_root);
    })
}

function set_ftp_root(root){
    let ftp_root = get_root_ftp(paths, 3);
    update_access_ftp_root.innerHTML = '<option>Choose...</option>';
    for (let i in ftp_root){
        let selected_status = '';
        if ((ftp_root[i] == root+'/') || (ftp_root[i] == root)){
            selected_status = 'selected'
        }
        update_access_ftp_root.innerHTML += `<option ${selected_status} value="${ftp_root[i]}">${ftp_root[i]}</option>`
    }
}

function update_access_update_page(){
    if (check_username_select(update_access_username)){
        post_data('/admin/user_information', {
            'username': update_access_username.value
        }).then(jsonObject => {
            if (jsonObject.status == 200){
                set_user_path(jsonObject.paths, jsonObject.ftp_root);
                set_checkbox_status(jsonObject.services);
            }
        })
    }
}

function edit_info(user){
    document.getElementById('update_user_access_btn').click();
    update_access_username.value = user;
    update_access_update_page()
}
window.edit_info = edit_info;

function set_mode(mode, status){
    post_data('/admin/set_mode', {
        "mode" : mode,
        "status": status
    }).then(jsonObject => {
        if (jsonObject.status === 200){
            settings_showAlert(`${mode} updated successfully` , 'alert-success')
        }
        else {
            settings_showAlert(jsonObject.text, 'alert-danger')
        }
    })
}

// dashboard 

function table_dashboard(){
    post_data('/admin/information_all_users', {'data': ''}).then((jsonObject) => {
        if (jsonObject.status == 200){
            const tbody = document.getElementById('tbody');
            tbody.innerHTML = '';
            username = [];
            for (let i in jsonObject.users){
                let num = parseInt(i) + 1;
                tbody.innerHTML += `<tr id="${i}"><th scope="row">${num}</th><td title="Click to edit the access" onclick="edit_info('${jsonObject.users[i][0]}')">${jsonObject.users[i][0]}</td> </tr>`
                username.push(jsonObject.users[i][0]);
                let tr = document.getElementById(i);
                for (let j=1; j< jsonObject.users[i].length; j++){
                    tr.innerHTML += _checkbox(jsonObject.users[i][j])
                }
            }
        }
    });
}
table_dashboard();

// Update Password 

let update_password_username_select = document.getElementById('username_passwordSelect');
let update_password_password = document.getElementById('password_change');
let update_password_password_verification = document.getElementById('password_verification_change');

document.getElementById('update_password_btn').addEventListener("click", () => {
    remove_valid_invalid(update_password_username_select);
    remove_valid_invalid(update_password_password);
    remove_valid_invalid(update_password_password_verification);

    update_password_password.value = '';
    update_password_password_verification.value = '';
    
    update_password_username_select.innerHTML = '<option selected>Choose...</option>';
    inner_username(update_password_username_select)
})

document.getElementById('password_save_btn').addEventListener("click", () => {
    let password_modal_close = document.getElementById('password_modal_close');

    if ((check_password(update_password_password)) &&
        (check_password_verification(update_password_password, update_password_password_verification)) && 
        (check_username_select(update_password_username_select)))
    {
        post_data('/admin/update_password', {'username': update_password_username_select.value,
        'password': update_password_password.value,
        'password_verification': update_password_password_verification.value}
        ).then((jsonObject) => {
            if (jsonObject.status == 200){
                showAlert(update_password_username_select.value + "'s password has been successfully changed.", 'alert-success')
            }
            else {
                showAlert(jsonObject.text, 'alert-danger')
            }
    
        });
        password_modal_close.click();
        close_menu.click();
    }
    
})

update_password_password.addEventListener('input', () => {
    check_password(update_password_password)
})

update_password_password_verification.addEventListener('input', () => {
    check_password_verification(update_password_password, update_password_password_verification);
})

update_password_username_select.addEventListener('change', () => {
    check_username_select(update_password_username_select);
})

// Update username

let update_username_username_select = document.getElementById('UserNameSelect');
let update_username_username_input = document.getElementById('input_username_change');

document.getElementById('update_username_btn').addEventListener("click", () => {
    remove_valid_invalid(update_username_username_select);
    remove_valid_invalid(update_username_username_input);

    update_username_username_input.value = '';
    update_username_username_select.innerHTML = '<option selected>Choose...</option>';

    post_data('/admin/get_all_users', {}).then(jsonObject => {
        for (let i in jsonObject['users']){
            update_username_username_select.innerHTML += `<option value="${jsonObject['users'][i][0]}">${jsonObject['users'][i][1]}</option>`
        }
    })
    
})

update_username_username_select.addEventListener('change', () => {
    check_input_select(update_username_username_select);
})

update_username_username_input.addEventListener('input', () => {
    check_username(update_username_username_input);
})

document.getElementById('btn_username_save_change').addEventListener("click", () => {
    let close_update_username = document.getElementById('btn_close_update_username');
    
    if ((check_input_select(update_username_username_select)) &&
        (check_username(update_username_username_input)))
    {
        
        post_data('/admin/update_username', {
            'id': update_username_username_select.value,
            'username': update_username_username_input.value
        }).then(jsonObject => {
            if (jsonObject.status == 200){
                table_dashboard();
                showAlert('Username changed successfully', 'alert-success')
            }
            else{
                showAlert(jsonObject.text, 'alert-danger')
            }
        })
        close_update_username.click();
        close_menu.click();
        
    }
})

// New User

let btn_new_user = document.getElementById('new_user_btn');
let new_user_username = document.getElementById('new_user_username');
let new_user_password = document.getElementById('new_user_password');
let new_user_password_verification = document.getElementById('new_user_password_verification');
let new_user_inputFtp_root = document.getElementById('new_user_inputFtp_root');
let new_user_paths = document.getElementById('new_user_paths');


document.getElementById('new_user_btn').addEventListener("click", () => {
    remove_valid_invalid(new_user_inputFtp_root);
    remove_valid_invalid(new_user_username);
    remove_valid_invalid(new_user_password);
    remove_valid_invalid(new_user_password_verification);

    paths = [];
    new_user_username.value = '';
    new_user_password.value = '';
    new_user_password_verification.value = '';
    new_user_paths.innerHTML = '';
    new_user_inputFtp_root.innerHTML = '<option selected>Choose...</option>';

    post_data('/admin/get_paths', {}).then(jsonObject => {
        paths = jsonObject.paths.split(',')

        for (let i in paths){
            new_user_paths.innerHTML += `<div class="form-check ms-1"><input class="form-check-input" type="checkbox" value="" id="path_checkbox${i}"><label class="form-check-label text-nowrap" for="path_checkbox${i}" id="path_label${i}">${paths[i]}</label></div>`;
        }
        let ftp_root = get_root_ftp(paths, 3);
        for (let i in ftp_root){
            new_user_inputFtp_root.innerHTML += `<option value="${ftp_root[i]}">${ftp_root[i]}</option>`
        }
    })
    
})

new_user_inputFtp_root.addEventListener('change', () => {
    check_input_select(new_user_inputFtp_root);
})

new_user_username.addEventListener('input', () => {
    check_username(new_user_username);
})

new_user_password.addEventListener('input', () => {
    check_password(new_user_password);
})

new_user_password_verification.addEventListener('input', () => {
    check_password_verification(new_user_password, new_user_password_verification)
})

document.getElementById('new_user_save_changes').addEventListener("click", () => {
    let new_user_close = document.getElementById('new_user_close');
    let ftp = document.getElementById('new_user_checkbox_ftp');
    let video = document.getElementById('new_user_checkbox_video');
    let audio = document.getElementById('new_user_checkbox_audio');
    let pdf = document.getElementById('new_user_checkbox_pdf');
    let receive = document.getElementById('new_user_checkbox_receive');
    let send = document.getElementById('new_user_checkbox_send');
    let system_control = document.getElementById('new_user_checkbox_system_control');
    let picture = document.getElementById('new_user_checkbox_picture');
    let ftp_store_file = document.getElementById('new_user_checkbox_store_file');
    let ftp_create_directory = document.getElementById('new_user_checkbox_create_directory');
    let user_paths = get_paths_user('path_checkbox', 'path_label' );

    
    if ((check_username(new_user_username)) && 
        (check_input_select(new_user_inputFtp_root)) &&
        (check_password(new_user_password)) && 
        (check_password_verification(new_user_password, new_user_password_verification))
    ){
        if (user_paths.length == 0){
            new_user_showAlert('You have to choose a path', 'alert-danger')
        }
        else {
            post_data('/admin/register', {
                'username': new_user_username.value,
                'password': new_user_password.value,
                'paths': user_paths.join(','),
                'ftp_root': new_user_inputFtp_root.value,
                'services': {
                    'ftp': checkbox_status(ftp),
                    'video': checkbox_status(video),
                    'audio': checkbox_status(audio),
                    'pdf': checkbox_status(pdf),
                    'receive': checkbox_status(receive),
                    'send': checkbox_status(send),
                    'system_control': checkbox_status(system_control),
                    'picture': checkbox_status(picture),
                    'ftp_create_directory': checkbox_status(ftp_create_directory),
                    'ftp_store_file': checkbox_status(ftp_store_file)
                }
            }).then(jsonObject => {
                if (jsonObject.status == 200){
                    table_dashboard();
                    new_user_close.click();
                    close_menu.click();
                    showAlert('User added successfully', 'alert-success');
                }
                else if ((jsonObject.status == 16) || (jsonObject.status == 15)){
                    new_user_showAlert(jsonObject.text + '\n' + jsonObject.problem, 'alert-danger');
                }
                else{
                    new_user_showAlert(jsonObject.text, 'alert-danger');
                }
            })
        }
    }
    
})

// Update Access

let update_access_username = document.getElementById('update_access_username');
let update_access_ftp_root = document.getElementById('update_access_inputFtp_root');
let update_access_checkbox_ftp = document.getElementById('update_access_checkbox_ftp');
let update_access_checkbox_receive = document.getElementById('update_access_checkbox_receive');
let update_access_checkbox_video = document.getElementById('update_access_checkbox_video');
let update_access_checkbox_send = document.getElementById('update_access_checkbox_send');
let update_access_checkbox_audio = document.getElementById('update_access_checkbox_audio');
let update_access_checkbox_system_control = document.getElementById('update_access_checkbox_system_control');
let update_access_checkbox_pdf = document.getElementById('update_access_checkbox_pdf');
let update_access_checkbox_picture = document.getElementById('update_access_checkbox_picture');
let update_access_checkbox_create_directory = document.getElementById('update_access_checkbox_create_directory');
let update_access_checkbox_store_file = document.getElementById('update_access_checkbox_store_file');
let update_access_paths = document.getElementById('update_access_paths');

document.getElementById('update_user_access_btn').addEventListener('click', () => {
    update_access_username.innerHTML = '<option selected>Choose...</option>'
    inner_username(update_access_username)
    update_access_ftp_root.innerHTML = ''
    update_access_paths.innerHTML = ''
    remove_valid_invalid(update_access_username)
    remove_valid_invalid(update_access_ftp_root)

})

update_access_username.addEventListener('change', () => {
    update_access_update_page()
})

document.getElementById('update_access_save_changes').addEventListener('click', () => {
    let close_update_access = document.getElementById('update_access_close')
    let user_paths = get_paths_user('update_access_path_checkbox', 'update_access_path_label' );
    if (check_username_select(update_access_username) &&
        check_input_select(update_access_ftp_root))
    {
        if (user_paths.length == 0){
            update_access_showAlert('You have to choose a path', 'alert-danger')
        }
        else {
            post_data('/admin/update_access', {
                'username': update_access_username.value,
                'paths': user_paths.join(','),
                'ftp_root': update_access_ftp_root.value,
                'services': {
                    'ftp': checkbox_status(update_access_checkbox_ftp),
                    'video': checkbox_status(update_access_checkbox_video),
                    'audio': checkbox_status(update_access_checkbox_audio),
                    'pdf': checkbox_status(update_access_checkbox_pdf),
                    'receive': checkbox_status(update_access_checkbox_receive),
                    'send': checkbox_status(update_access_checkbox_send),
                    'system_control': checkbox_status(update_access_checkbox_system_control),
                    'picture': checkbox_status(update_access_checkbox_picture),
                    'ftp_create_directory': checkbox_status(update_access_checkbox_create_directory),
                    'ftp_store_file': checkbox_status(update_access_checkbox_store_file)
                }
            }).then(jsonObject => {
                if (jsonObject.status == 200){
                    table_dashboard();
                    close_update_access.click();
                    close_menu.click();
                    showAlert('User updated successfully', 'alert-success');
                }
                else if ((jsonObject.status == 16) || (jsonObject.status == 15)){
                    update_access_showAlert(jsonObject.text + '\n' + jsonObject.problem, 'alert-danger');
                }
                else{
                    update_access_showAlert(jsonObject.text, 'alert-danger');
                }
            })
        }
    }
})

// Update system control password

let system_control_password = document.getElementById('system_control_update_password_password')
let system_control_password_verification = document.getElementById('system_control_update_password_verification')

document.getElementById('system_control_update_password_btn').addEventListener('click', () => {
    remove_valid_invalid(system_control_password);
    remove_valid_invalid(system_control_password_verification);
    system_control_password.value = '';
    system_control_password_verification.value = '';
})

system_control_password.addEventListener('input', () => {
    check_password(system_control_password)
})
system_control_password_verification.addEventListener('input', () => {
    check_password_verification(system_control_password, system_control_password_verification)
})

document.getElementById('system_control_update_password_save_btn').addEventListener('click', () => {
    let system_control_update_password_close = document.getElementById('system_control_update_password_modal_close');
    if (check_password(system_control_password) && 
        check_password_verification(system_control_password, system_control_password_verification))
    {
        post_data('/admin/system_control_password', {
            'password': system_control_password.value,
            'password_verification': system_control_password_verification.value
        }).then(jsonObject => {
            if (jsonObject.status == 200){
                system_control_update_password_close.click();
                close_menu.click();
                showAlert('Password changed successfully', 'alert-success')
            }
            else{
                update_access_showAlert(jsonObject.text, 'alert-danger');
            }
        })

    }
})

// settings

let setting_checkbox_guest_mode = document.getElementById("settings_checkbox_gust_mode")
let setting_checkbox_login = document.getElementById("settings_checkbox_login")
let setting_checkbox_ftp = document.getElementById("settings_checkbox_ftp")
let settings_checkbox_ftp_create_directory = document.getElementById("settings_checkbox_ftp_create_directory")
let settings_checkbox_ftp_store_file = document.getElementById("settings_checkbox_ftp_store_file")
let settings_checkbox_run_background = document.getElementById("settings_checkbox_run_background")
let settings_input_web_app_port = document.getElementById("input_web_app_port")
let settings_input_ftp_server_port = document.getElementById("input_ftp_server_port")
let settings_inputFtp_root = document.getElementById("settings_inputFtp_root")
let settings_advance_ftp_root = 2;

document.getElementById("settings_btn").addEventListener('click', () => {
    post_data('/admin/get_mode', {}).then(jsonObject => {
        set_checkbox_settings(jsonObject['modes'])
    })
    post_data('/admin/get_port', {'type': 'web_app'}).then(jsonObject => {
        if (jsonObject.status === 200){
            settings_input_web_app_port.value = jsonObject['port']
        }
        else {
            settings_showAlert(jsonObject.text, 'alert-danger')
        }
    })
    post_data('/admin/get_port', {'type': 'ftp_server'}).then(jsonObject => {
        if (jsonObject.status === 200){
            settings_input_ftp_server_port.value = jsonObject['port']
        }
        else {
            settings_showAlert(jsonObject.text, 'alert-danger')
        }
    })
    settings_inputFtp_root.innerHTML = '<option selected>Choose...</option>';
    post_data('/admin/get_ftp_root', {
        'advance': settings_advance_ftp_root,
        'username': ''
    }).then(jsonObject => {
        for (let i in jsonObject['roots']){
            settings_inputFtp_root.innerHTML += `<option value="${jsonObject['roots'][i]}">${jsonObject['roots'][i]}</option>`
        }
    })
})

setting_checkbox_guest_mode.addEventListener('change', () => {
    set_mode('guest', checkbox_status(setting_checkbox_guest_mode))
})

setting_checkbox_login.addEventListener('change', () => {
    set_mode('login', checkbox_status(setting_checkbox_login))
})

setting_checkbox_ftp.addEventListener('change', () => {
    set_mode('ftp', checkbox_status(setting_checkbox_ftp))
})

settings_checkbox_ftp_create_directory.addEventListener('change', () => {
    set_mode('ftp_create_directory', checkbox_status(settings_checkbox_ftp_create_directory))
})

settings_checkbox_ftp_store_file.addEventListener('change', () => {
    set_mode('ftp_store_file', checkbox_status(settings_checkbox_ftp_store_file))
})

settings_checkbox_run_background.addEventListener('change', () => {
    set_mode('run_background', checkbox_status(settings_checkbox_run_background))
})

settings_input_web_app_port.addEventListener('change', () => {
    if (valid_and_invalid(settings_input_web_app_port,
        settings_input_web_app_port.value !== settings_input_ftp_server_port.value)){
        post_data('/admin/set_port', {
            'type': 'web',
            'port': settings_input_web_app_port.value
        }).then(jsonObject => {
            if (jsonObject.status === 200){
                settings_showAlert('The web app port has been updated successfully', 'alert-success')
            }
            else {
                settings_showAlert(jsonObject.text, 'alert-danger')
            }
        })
    }
})

settings_input_ftp_server_port.addEventListener('change', () => {
    if (valid_and_invalid(settings_input_ftp_server_port,
        settings_input_ftp_server_port.value !== settings_input_web_app_port.value)){
        post_data('/admin/set_port', {
            'type': 'ftp',
            'port': settings_input_ftp_server_port.value
        }).then(jsonObject => {
            if (jsonObject.status === 200){
                settings_showAlert('The ftp server port has been updated successfully', 'alert-success')
            }
            else {
                settings_showAlert(jsonObject.text, 'alert-danger')
            }
        })
    }
})

settings_inputFtp_root.addEventListener('change', () => {
    post_data('/admin/set_ftp_root', {
        'root' : settings_inputFtp_root.value,
        'advance': settings_advance_ftp_root,
        'username': ''
    }).then(jsonObject => {
        if (jsonObject.status === 200){
            settings_showAlert('The FTP server root has been updated successfully', 'alert-success')
        }
    })
})