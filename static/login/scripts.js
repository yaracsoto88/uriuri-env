function login() {
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    })
        .then(response => manage_login_data(response, email))
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
}

function signin() {
    let username = document.getElementById('username').value;
    let mail = document.getElementById('mail').value;
    let password = document.getElementById('password').value;
    let password_confirmation = document.getElementById('passwordconfirm').value;

    if (password.length < 6) {
        alert("La contraseña debe tener mínimo 6 caracteres");
        return;
    }

    if (password != password_confirmation) {
        alert("Las contraseñas son diferentes");
        return;
    }

    if (!validateEmail(mail)) {
        alert("Pon un mail correcto");
        return;
    }

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            email: mail,
            password: password,
        }),
    })
        .then(response => manage_register_response(response, mail))
        .then(data => console.log(data))
        .catch((error) => {
            console.error('Error:', error);
        });
}

function validateEmail(email) {
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function manage_register_response(response, email) {
    response.json().then(data => {
        if (data.message == 'User created') {
            localStorage.setItem('email', email);
            localStorage.setItem('alerta', "Usuario creado correctamente");
            window.location.href = '/static/friends/friends.html';
        } else {
            alert("Error al crear el usuario");
        }
    });
}

function manage_login_data(response, email) {
    response.json().then(data => {
        if (data.message == 'Login successful') {
            localStorage.setItem('email', email);
            console.log(localStorage.getItem('email'));
            localStorage.setItem('alerta', "Usuario loggeado correctamente");
            window.location.href = '/static/friends/friends.html';
        } else {
        }
    });
}
//     }