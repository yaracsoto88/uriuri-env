function login(){
    console.log('login');
    var email = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    console.log(username);
    console.log(password);

    fetch('http://localhost:8000/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch((error) => {
      console.error('Error:', error);
    });
}