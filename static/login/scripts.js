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
function singin(){
    let email = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let password_confirmation= document.getElementById('passwordconfirm').value;
    if(password!= password_confirmation){
        alert("las contraseñas son diferentes");
    }

    fetch('/register', {
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
