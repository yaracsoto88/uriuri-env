window.onload = function() {
    // Asegúrate de que 'username' esté definido en algún lugar de tu código
    let username = "yara"; 

    fetch('/friends', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
        }),
    })
    .then(response => manage_friends_response(response))
    .catch((error) => {
      console.error('Error:', error);
    });
}

function manage_friends_response(response){
    response.json().then(data => {
        // Usa 'let' para declarar la variable 'friend' en el bucle for...of
        for (let friend of data.friends){
            let friendDiv = document.createElement("div");
            friendDiv.innerHTML = friend;
            document.getElementById('friends').appendChild(friendDiv);
        }
    }).catch((error) => {
      console.error('Error:', error);
    });
}