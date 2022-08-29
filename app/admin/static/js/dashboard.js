let username = [];
const password_patern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/gm;
let close_menu = document.getElementById('close_menu');

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


post_data('/admin/information_all_users', {'data': ''}).then((jsonObject) => {
    if (jsonObject.status == 200){
        const tbody = document.getElementById('tbody');
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
