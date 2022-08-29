let username = [];
const password_patern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/gm;
const username_pattern = /^(?=.{4,20}$)[a-zA-Z0-9]+$/gm;
let close_menu = document.getElementById('close_menu');

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

function showAlert(message, typeAlert){
    document.getElementById('myAlert').innerHTML = '<div class="alert ' + typeAlert + '">'+message+'</div>';
        setTimeout(function(){
            document.getElementById('myAlert').innerHTML = '';
        }, 6000);
}

function _checkbox(status){
    if (status == '1'){
        return '<td><input type="checkbox" disabled checked></td>'
    }
    return '<td><input type="checkbox" disabled></td>'
}


function table_dashboard(){
    post_data('/admin/information_all_users', {'data': ''}).then((jsonObject) => {
        if (jsonObject.status == 200){
            const tbody = document.getElementById('tbody');
            tbody.innerHTML = '';
            username = [];
            for (let i in jsonObject.users){
                tbody.innerHTML += '<tr id="'+ i +'"><th scope="row">' + i +'</th><td>'+ jsonObject.users[i][0] + '</td> </tr>'
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

document.getElementById('update_password_btn').addEventListener("click", () => {
    let input_username = document.getElementById('username_passwordSelect');
    input_username.innerHTML = '<option selected>Choose...</option>';
    for (let i in username){
        input_username.innerHTML += '<option value="'+ username[i] + '">' + username[i] +'</option>'
    }
})

document.getElementById('password_save_btn').addEventListener("click", () => {
    let user_name = document.getElementById('username_passwordSelect');
    let password = document.getElementById('password_change');
    let password_verification = document.getElementById('password_verification_change');
    let password_modal_close = document.getElementById('password_modal_close');
    if (password.value.match(password_patern)){
        if (password.value == password_verification.value){
            if (username.includes(user_name.value)){
                post_data('/admin/update_password', {'username': user_name.value,
                'password': password.value,
                'password_verification': password_verification.value}
                ).then((jsonObject) => {
                    if (jsonObject.status == 200){
                        showAlert(user_name.value + "'s password has been successfully changed.", 'alert-success')
                    }
                    else {
                        showAlert(jsonObject.text, 'alert-danger')
                    }
            
                });
                password.value = '';
                password_verification.value = '';
                password.classList.remove('is-valid');
                password_verification.classList.remove('is-valid');
                user_name.classList.remove('is-valid');
                password_modal_close.click();
                close_menu.click();
            }
            else {
                user_name.classList.add('is-invalid');
            }
        }
        else {
            password_verification.classList.add('is-invalid');
        }
    }else {
        password.classList.add('is-invalid');
    }
})
document.getElementById('password_change').addEventListener('input', () => {
    let password = document.getElementById('password_change');
    password.classList.remove('is-invalid');
    password.classList.remove('is-valid');
    if (password.value.match(password_patern)){
        password.classList.add('is-valid');
    }
    else {
        password.classList.add('is-invalid');
    }
})
document.getElementById('password_verification_change').addEventListener('input', () => {
    let password_verification_change = document.getElementById('password_verification_change');
    let password = document.getElementById('password_change');
    password_verification_change.classList.remove('is-invalid');
    password_verification_change.classList.remove('is-valid');
    if ((password_verification_change.value == password.value) && (password.value.match(password_patern))){
        password_verification_change.classList.add('is-valid');
    }
    else {
        password_verification_change.classList.add('is-invalid');
    }
})
document.getElementById('username_passwordSelect').addEventListener('change', () => {
    let user_name = document.getElementById('username_passwordSelect');
    user_name.classList.remove('is-invalid');
    user_name.classList.remove('is-valid');
    if (username.includes(user_name.value)){
        user_name.classList.add('is-valid');
    }
    else {
        user_name.classList.add('is-invalid');
    } 
})

// Update username

document.getElementById('update_username_btn').addEventListener("click", () => {
    let input_username = document.getElementById('UserNameSelect');
    let user_name = document.getElementById('input_username_change');
    remove_valid_invalid(input_username);
    remove_valid_invalid(user_name);
    user_name.value = '';
    input_username.innerHTML = '<option selected>Choose...</option>';
    post_data('/admin/get_all_users', {}).then(jsonObject => {
        for (let i in jsonObject['users']){
            input_username.innerHTML += '<option value="'+ jsonObject['users'][i][0] + '">' + jsonObject['users'][i][1] +'</option>'
        }
    })
    
})

document.getElementById('UserNameSelect').addEventListener('change', () => {
    let user_name = document.getElementById('UserNameSelect');

    remove_valid_invalid(user_name);

    if (user_name.value !== 'Choose...'){
        user_name.classList.add('is-valid');
    }
    else {
        user_name.classList.add('is-invalid');
    } 
})

document.getElementById('input_username_change').addEventListener('input', () => {
    let user_name = document.getElementById('input_username_change');

    remove_valid_invalid(user_name);
    
    if (user_name.value.match(username_pattern)){
        user_name.classList.add('is-valid');
    }
    else {
        user_name.classList.add('is-invalid');
    }
})

document.getElementById('btn_username_save_change').addEventListener("click", () => {
    let input_username = document.getElementById('UserNameSelect');
    let user_name = document.getElementById('input_username_change');
    let close_update_username = document.getElementById('btn_close_update_username');
    
    if (input_username.value !== 'Choose...'){
        input_username.classList.add('is-valid');
        if (user_name.value.match(username_pattern)){
            user_name.classList.add('is-valid');
            post_data('/admin/update_username', {
                'id': input_username.value,
                'username': user_name.value
            }).then(jsonObject => {
                if (jsonObject.status == 200){
                    showAlert('Username changed successfully', 'alert-success')
                }
                else{
                    showAlert(jsonObject.text, 'alert-danger')
                }
                close_update_username.click();
                close_menu.click();
            })
        }
        else {
            user_name.classList.add('is-invalid');
        }
    }
    else {
        input_username.classList.add('is-invalid');
    } 
})