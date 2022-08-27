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
        for (var i in jsonObject.users){
            tbody.innerHTML += '<tr id="'+ i +'"><th scope="row">' + i +'</th><td>'+ jsonObject.users[i][0] + '</td> </tr>'
            var tr = document.getElementById(i);
            for (var j=1; j< jsonObject.users[i].length; j++){
                tr.innerHTML += _checkbox(jsonObject.users[i][j])
            }
        }
    }

});



