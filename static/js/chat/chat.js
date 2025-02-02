window.onload = function() {
    const chatContainer = document.getElementById('messagesContainer');
    chatContainer.scrollTop = chatContainer.scrollHeight;
};

function escapeHTML(str) {
    return str.replace(/&/g, "&amp;")
              .replace(/</g, "&lt;")
              .replace(/>/g, "&gt;")
              .replace(/"/g, "&quot;")
              .replace(/'/g, "&#039;");
}

document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.getElementById("messagesContainer");
    const messageInput = document.getElementById("id_message_send_input");
    const sendButton = document.getElementById("id_message_send_button");

    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomPk}/`);

    chatSocket.onopen = () => console.log("Connected to WebSocket");
    chatSocket.onclose = () => console.log("Disconnected from WebSocket");

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        addMessage(data.username, data.message, data.avatar, data.username === user_username ? false : true);
    };

    sendButton.onclick = sendMessage;
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        chatSocket.send(JSON.stringify({ message: message, username: user_username, avatar: avatar_url}));
        messageInput.value = "";
    }

    function addMessage(username, message, avatar, isIncoming) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", isIncoming ? "other-message" : "own-message");

        messageDiv.innerHTML = `
            <img src="${avatar}" alt="Avatar" class="avatar">
            <div class="message-bubble bg-primary border border-light text-dark">
                <div class="message-header">
                    ${username}
                </div>
                <p>${escapeHTML(message)}<span class="timestamp d-flex">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span></p>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});