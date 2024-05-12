function login(){
    console.log('login');
    var email = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    console.log(email);
    console.log(password);

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
    .then(response => console.log(response.json()))
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
}
function signin(){
    let username = document.getElementById('username').value;
    let mail = document.getElementById('mail').value;
    let password = document.getElementById('password').value;
    let password_confirmation= document.getElementById('passwordconfirm').value;
        
    if (password.length<6){
        alert("la contraseña debe tener minimo 6 caracteres");
        return;
    }

    if(password!= password_confirmation){
        alert("las contraseñas son diferentes");
        return;
    }

    if (!validateEmail(mail)){
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
    .then(response =>manage_register_response(response))
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
}

function validateEmail(email){
    var re = /\S+@\S+\.\S+/;
    return re.test(email);
}

function manage_register_response(response){
    response.json().then(data => {
        if (data.message == 'User created'){
            alert("Usuario creado correctamente");
            window.location.href = '/chat';
        }else{
            alert("Error al crear el usuario");
        }
    });
}

