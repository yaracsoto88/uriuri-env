window.onload = function () {

    let email = localStorage.getItem('email')
    console.log(email)
    fetch('/friends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
        }),
    })
        .then(response => manage_friends_response(response))
        .catch((error) => {
            console.error('Error:', error);
        });
}

async function manage_friends_response(response) {
    try {
        let data = await response.json();
        // Crear una tabla
        let table = document.createElement("table");

        // Crear la fila de encabezado
        let thead = document.createElement("thead");
        let headerRow = document.createElement("tr");
        let th = document.createElement("th");
        th.innerHTML = "Friends";
        headerRow.appendChild(th);
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Crear el cuerpo de la tabla
        let tbody = document.createElement("tbody");

        // Añadir cada amigo como una nueva fila en la tabla
        for (let friend of data) {
            let row = document.createElement("tr");
            let td = document.createElement("td");
            // friend 
            console.log(friend)
            let id_amigo = await get_friend_id(friend);
            // Crear un enlace y establecer su href
            let a = document.createElement("a");
            a.href = "/static/chat/chat.html?id=" + id_amigo;
            a.innerHTML = friend;

            // Agregar el enlace a la celda
            td.appendChild(a);
            row.appendChild(td);
            tbody.appendChild(row);

            table.appendChild(tbody);
        }
        // Añadir la tabla al elemento 'friends' en el DOM
        document.getElementById('friends').innerHTML = '';
        document.getElementById('friends').appendChild(table);
    } catch (error) {
        console.error('Error:', error);
    }
}

async function get_friend_id(username) {
    try {
        let response = await fetch('/idfriend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
            }),
        });
        let data = await response.json();
        console.log(data);
        return data  
    } catch (error) {
        console.error('Error:', error);
    }
}


