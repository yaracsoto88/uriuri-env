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
