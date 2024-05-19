window.onload = async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const id_friend = urlParams.get('id');
    const email = localStorage.getItem('email');
    
    if (id_friend) {
        try {
            let response = await fetch(`/mensajes?emailUser=${email}&idfriend=${id_friend}`);
            if (response.ok) {
                let messages = await response.json();
                let messagesDiv = document.getElementById('messages');
                messagesDiv.innerHTML = '';

                messages.forEach(message => {
                    let messageElement = document.createElement('p');
                    messageElement.textContent = message.message + " sender:id: " + message.sender_id;
                    messagesDiv.appendChild(messageElement);
                });

                // Initialize WebSocket
                var ws = new WebSocket(`ws://${window.location.host}/ws`);
                ws.onmessage = function(event) {
                    let messageElement = document.createElement('p');
                    messageElement.textContent = event.data;
                    messagesDiv.appendChild(messageElement);
                };

                document.querySelector('form').onsubmit = function(event) {
                    let input = document.getElementById('messageText');
                    ws.send(JSON.stringify({
                        sender: localStorage.getItem('email'),
                        receiver: urlParams.get('id'),
                        message: input.value
                    }));
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
