var sendMode = true;

document.addEventListener("contextmenu", (event) => event.preventDefault());

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

function addContextMenu() {
    document.querySelectorAll('.message-bubble.own-msg')
        .forEach(msg => msg.addEventListener('contextmenu', function(event) {
            event.preventDefault();
            event.stopPropagation();
            
            let messageId = this.getAttribute('data-message-id');
            
            if (!msg.classList.contains('own-msg')) return;
            
            messageOptions(event, messageId);
        }));
}

function messageOptions(e, messageId) {
    let menu = document.getElementById('message-options')
    
    menu.style.top = `${event.clientY <= 850 ? event.clientY : event.clientY - 125}px`;
    menu.style.left = `${event.clientX <= 1350 ? event.clientX - 325 : event.clientX - 525}px`;
    menu.style.display = "block";
    menu.setAttribute('message-id', messageId);
}

document.addEventListener("click", function () {
    document.getElementById("message-options").style.display = "none";
});

document.getElementById('edit-message').addEventListener('click', function () {
    let messageId = document.getElementById('message-options').getAttribute('message-id');
    sendMode = false;
    
    document.querySelector(".chat-input-container").style.display = "none";
    document.querySelector(".chat-edit-container").style.display = "flex";
    document.getElementById("id_message_send_input").value = "";
    document.getElementById("id_message_edit_input").value = document.querySelector(`[data-message-id="${messageId}"].content-message`).innerText;
});


document.addEventListener("DOMContentLoaded", function () {
    const messagesContainer = document.getElementById("messagesContainer");
    const messageInput = document.getElementById("id_message_send_input");
    const sendButton = document.getElementById("id_message_send_button");
    const editInput = document.getElementById('id_message_edit_input');
    const editButton = document.getElementById('id_message_edit_button');
    const imageButton = document.getElementById('id_message_image_button');
    const imageInput = document.getElementById('id_message_image_input');
    
    let selectedImage = null;
    
    imageButton.addEventListener('click', () => {
        imageInput.click();
    });
    
    imageInput.addEventListener("change", (event) => {
        const files = Array.from(event.target.files);
        const filePreview = document.getElementById('file-preview');
        
        filePreview.innerHTML = '';
        selectedImage = null;
        
        files.forEach((file, index) => {
            if (!file.type.startsWith('image/')) {
                console.warn(`Файл ${file.name} не является изображением и не будет добавлен.`);
                return;
            }
    
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');
    
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            fileItem.appendChild(img);
    
            const fileName = document.createElement('span');
            fileName.textContent = file.name;
            fileItem.appendChild(fileName);
    
            const removeBtn = document.createElement('span');
            removeBtn.textContent = '✖';
            removeBtn.classList.add('remove-file');
            removeBtn.addEventListener('click', () => {
                fileItem.remove();
                selectedImage = null;
                imageInput.value = '';
            });
    
            fileItem.appendChild(removeBtn);
            filePreview.appendChild(fileItem);
    
            if (!selectedImage) {
                const reader = new FileReader();
                reader.onloadend = () => {
                    selectedImage = reader.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });

    addContextMenu();

    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const chatSocket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomPk}/`);
    console.log(protocol);

    chatSocket.onopen = () => console.log("Connected to WebSocket");
    chatSocket.onclose = () => console.log("Disconnected from WebSocket.");

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        
        if (data.type === "update_chat_list") {
            updateChatList(data.chat_id, data.chat_name, data.last_message, data.chat_avatar);
        } else if (data.type === "message_deleted") {
            deleteMessage(data.message_id);
        } else if (data.type === "edit_message") {
            updateMessage(data.message_id, data.new_content);
        } else {
            addMessage(data.username, data.message, data.avatar, data.message_id, data.image_url, data.username === user_username ? false : true);
        }
    };

    sendButton.onclick = sendMessage;
    messageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            if (sendMode) sendMessage();
        }
    });
    
    editButton.onclick = editMessage;
    editInput.addEventListener('keypress', function (event) {
        if (event.key === "Enter") {
            if (!sendMode) editMessage();
        }
    })

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message && !selectedImage) return;

        chatSocket.send(JSON.stringify({
            'type': 'send_message',
            'message': message,
            'image': selectedImage,
            'username': user_username,
            'avatar': avatar_url
        }));
        
        messageInput.value = "";
        selectedImage = null;
        document.getElementById('file-preview').innerHTML = '';
    }
    
    function editMessage() {
        let message = editInput.value.trim();
        if (!message) return;
        
        let messageId = document.getElementById("message-options").getAttribute('message-id');
        if (!messageId) return;
        
        sendMode = true;
        document.querySelector(".chat-input-container").style.display = "flex";
        document.querySelector(".chat-edit-container").style.display = "none";
        document.getElementById("id_message_send_input").value = "";
        document.getElementById("id_message_edit_input").value = "";
               
        chatSocket.send(JSON.stringify({
            'type': 'edit_message',
            'message_id': messageId,
            "new_content": message
        }));
    }

    function addMessage(username, message, avatar, pk, imageURL, isIncoming) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", isIncoming ? "other-message" : "own-message");
        messageDiv.setAttribute('data-message-id', pk);

        messageDiv.innerHTML = `
            <img src="${avatar}" alt="Avatar" class="avatar">
            <div class="message-bubble ${isIncoming ? 'other-msg bg-success' : 'own-msg bg-info'} border border-dark text-dark" data-message-id="${pk}">
                <div class="message-header">
                    ${username}
                </div>
                ${ imageURL ? '<img src="' + imageURL + '" style="max-width: 100%;">' : '' }
                <p><span class="content-message" data-message-id="${pk}">${escapeHTML(message)}</span><span class="timestamp d-flex">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span></p>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        addContextMenu();
    }
    
    document.getElementById('delete-message').addEventListener('click', function () {
        let messageId = document.getElementById('message-options').getAttribute('message-id');
        
        chatSocket.send(JSON.stringify({
            'type': 'delete_message',
            'message_id': messageId,
        }))
    });
    
    function deleteMessage(messageId) {
        let msgElement = document.querySelector(`[data-message-id="${messageId}"].chat-message`)
        if (msgElement) msgElement.remove();
    }
    
    function updateMessage(messageId, new_content) {
        let msgElement = document.querySelector(`[data-message-id="${messageId}"].content-message`)
        if (msgElement) msgElement.textContent = new_content;
    }
    
    function updateChatList(chatId, chatName, lastMessage, chatAvatar) {
        const chatListContainer = document.querySelector('.chat-list .row')
        
        let existingChat = document.querySelector(`[data-chat-id="${chatId}"]`);
        
        if (existingChat) {
            existingChat.querySelector('.list-msg').textContent = lastMessage;
        } else {
            const chatElement = document.createElement("a");
            chatElement.href = `/chat/${chatId}/`;
            chatElement.classList.add('btn', 'btn-primary', 'chat-el', 'mt-2');
            chatElement.setAttribute('data-chat-id', chatId);
            
            chatElement.innerHTML = `
                <div class='row'>
                    <div class='col-3'>
                        <img src="${chatAvatar}" width='56' height='56' class='rounded-circle'>
                    </div>
                    <div class='col-9'>
                        <div class='row'>
                            <div class='col-12'>${chatName}</div>
                            <div class='col-12 list-msg'>${lastMessage}</div>
                        </div>
                    </div>
                </div>
            `;
            
            chatListContainer.prepend(chatElement);
        }
    }
});
