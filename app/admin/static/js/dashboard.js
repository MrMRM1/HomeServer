let username = [];
const password_patern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/gm;

function _checkbox(status){
    if (status == '1'){
        return '<td><input type="checkbox" disabled checked></td>'
    }
    return '<td><input type="checkbox" disabled></td>'
}

fetch('/admin/get_all_users', {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'data': ''}),
}).then((response) => {
        return response.json();
}).then((jsonObject) => {
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



