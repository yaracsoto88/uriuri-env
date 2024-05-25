window.onload = function () {
    let email = localStorage.getItem('email');
    console.log(email);

    fetch('/friends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
        }),
    })
    .then(response => {
        manage_friends_response(response);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    loadAlert();
	get_friend_request(email);
}

async function manage_friends_response(response) {
    try {
        let data = await response.json();
        // Crear una tabla con Bulma
        let table = document.createElement("table");
        table.classList.add("table", "is-fullwidth", "is-bordered", "is-striped", "is-hoverable");

        // Crear el cuerpo de la tabla
        let tbody = document.createElement("tbody");

        // Añadir cada amigo como una nueva fila en la tabla
        for (let friend of data) {
            let row = document.createElement("tr");
            let td = document.createElement("td");
            td.classList.add("has-text-centered", "has-background-light"); // Fondo claro y texto centrado para las celdas
            // Obtener ID del amigo
            console.log(friend);
            let id_amigo = await get_friend_id(friend);
            console.log(id_amigo);
            // Crear un enlace y establecer su href
            let a = document.createElement("a");
            a.href = "/static/chat/chat.html?id=" + id_amigo;
            console.log("/static/chat/chat.html?id=" + id_amigo)
            a.innerHTML = friend;
            a.classList.add("has-text-link", "has-text-weight-bold"); // Enlace estilizado con color de enlace y texto en negrita

            // Agregar el enlace a la celda
            td.appendChild(a);
            row.appendChild(td);
            tbody.appendChild(row);
        }
        table.appendChild(tbody);

        // Añadir la tabla al elemento 'friends' en el DOM
        let friendsContainer = document.getElementById('friends');
        friendsContainer.innerHTML = '';
        friendsContainer.appendChild(table);
    } catch (error) {
        console.error('Error:', error);
    }
}




async function get_friend_request(email) {
    fetch('/friend_request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
        }),
    })
    .then(response => {
        manage_friend_requests_response(response);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

async function manage_friend_requests_response(response){
    try {
        let data = await response.json();
        let friendRequestContainer = document.getElementById('friend_request');
        friendRequestContainer.innerHTML = '';
        console.log("----------------------")
        console.log(data)
        console.log(data.size)
        if (data.length == 0){
            let box_container= document.getElementById("box_requests");
            box_container.style.display = "none";
            return
        }
        for (let friend of data) {
            let friendRequest = document.createElement('div');
            friendRequest.classList.add("notification", "is-info");
            friendRequest.innerHTML = friend;
            friendRequestContainer.appendChild(friendRequest);
        }
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
        return data;  
    } catch (error) {
        console.error('Error:', error);
    }
}

function loadAlert() {
    let alert = localStorage.getItem('alerta');
    console.log(alert);
    if (alert == null) {
        return;
    }
    Toastify({
        text: alert,
        duration: 3000,
        style: {
            background: "linear-gradient(to right, #00b09b, #96c93d)"
        }
    }).showToast();
    localStorage.removeItem('alerta');
}

function logout() {
    localStorage.removeItem('email');
    window.location.href = '/static/login/index.html';
}

function showaddFriend() {
    document.getElementById('addFriend').style.display = 'block';
}

async function addFriend() {
    let email = localStorage.getItem('email');
    let friend = document.getElementById('friend').value;
    console.log(friend);
    console.log(email);
    fetch('/addfriend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            friend: friend,
        }),
    })
    .then(response => manage_add_friends_response(response))
    .catch((error) => {
        console.error('Error:', error);
    });
}

 async function manage_add_friends_response(response) {
    response.json().then(data => {
        console.log(data);
        localStorage.setItem('alerta', data.message);
        window.location.href = '/static/friends/friends.html';
    });
}
