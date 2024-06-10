window.onload = async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id_friend = urlParams.get('id');
    const email = localStorage.getItem('email');
    
    if (id_friend) {
        try {
            let responseName = await fetch(`/get_name`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: id_friend,
                }),
            });

            if (responseName.ok) {
                let friendData = await responseName.json();
                document.getElementById('titleName').textContent = friendData;
            } else {
                console.error('Error fetching friend name:', responseName.statusText);
            } 
            let response = await fetch(`/mensajes?emailUser=${email}&idfriend=${id_friend}`);
            if (response.ok) {
                let messages = await response.json();
                let messagesDiv = document.getElementById('messages');
                messagesDiv.innerHTML = '';

                messages.forEach(message => {
                    let messageElement = document.createElement('article');
                    messageElement.classList.add('message');
                    messageElement.classList.add(message.sender_id !== id_friend ? 'is-primary' : 'is-info');

                    let messageBody = document.createElement('div');
                    messageBody.classList.add('message-body');
                    messageBody.textContent = message.message;

                    messageElement.appendChild(messageBody);
                    messagesDiv.appendChild(messageElement);
                });
                var messagesBox = document.getElementById('messages');
                messagesBox.scrollTop = messagesBox.scrollHeight;

                // Initialize WebSocket with user's email
                var ws = new WebSocket(`ws://${window.location.host}/ws/${email}`);
                ws.onmessage = function(event) {
                    let messageElement = document.createElement('article');
                    messageElement.classList.add('message', 'is-info');

                    let messageBody = document.createElement('div');
                    messageBody.classList.add('message-body');
                    messageBody.textContent = event.data;
                    
                    messageElement.appendChild(messageBody);
                    messagesDiv.appendChild(messageElement);
                    var messagesBox = document.getElementById('messages');
                    messagesBox.scrollTop = messagesBox.scrollHeight;
                };

                document.querySelector('form').onsubmit = function(event) {
                    let input = document.getElementById('messageText');
                    if (input.value.trim() === '') {
                        input.value = '';
                        event.preventDefault();
                        return;
                    }
                    let messageElement = document.createElement('article');
                    messageElement.classList.add('message', 'is-primary');

                    let messageBody = document.createElement('div');
                    messageBody.classList.add('message-body');
                    messageBody.textContent = input.value;

                    messageElement.appendChild(messageBody);
                    messagesDiv.appendChild(messageElement);
                    ws.send(JSON.stringify({
                        sender: localStorage.getItem('email'),
                        receiver: urlParams.get('id'),
                        message: input.value
                    }));
                    var messagesBox = document.getElementById('messages');
                    messagesBox.scrollTop = messagesBox.scrollHeight;
                    input.value = '';
                    event.preventDefault();
                };
            } else {
                console.error('Error fetching messages:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        console.error('No ID provided in URL');
    }
}
function logout() {
    localStorage.removeItem('email');
    localStorage.setItem('alerta', "Sesión cerrada correctamente");
    window.location.href = '/static/login/index.html';
}

function back_friends() {
    window.history.back();
}