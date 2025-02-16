document.getElementById('search-input').addEventListener('input', function () {
    let query = this.value.trim();
    
    if (query.length > 0) {
        fetch(`/chat/search_users/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                let resultsContainer = document.getElementById('results');
                resultsContainer.innerHTML = '';
                
                data.users.forEach(user => {
                    let a = document.createElement('a');
                    a.href = `/chat/get/${user.pk}/`;
                    a.className = "list-group-item list-group-item-action chat-link mt-2";
                    a.textContent = user.username;
                    resultsContainer.appendChild(a);
                });
            });
    } else {
        document.getElementById('results').innerHTML = '';
    }
});

document.getElementById('friends-input').addEventListener('input', function () {
    let query = this.value.trim();
    let groupId = document.getElementById('addGroupMember').dataset.groupId;
    
    if (query.length > 0) {
        fetch(`/chat/search_friends/?q=${query}&group_id=${groupId}`)
            .then(response => response.json())
            .then(data => {
                let resultsContainer = document.getElementById('resultsFriends');
                resultsContainer.innerHTML = '';
                
                data.users.forEach(user => {
                    let a = document.createElement('a');
                    a.className = "list-group-item list-group-item-action chat-link mt-2";
                    a.textContent = user.username;
                    a.dataset.userId = user.pk;
                    a.addEventListener('click', function () {
                        addUserToGroup(user.pk);
                    });
                    resultsContainer.appendChild(a);
                });
            });
    } else {
        document.getElementById('results').innerHTML = '';
    }
});

function addUserToGroup(userId) {
    let groupId = document.getElementById('addGroupMember').dataset.groupId;
    
    fetch(`/chat/add_to_group/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ user_id: userId, group_id: groupId })
    })
        .then(response => {
            location.reload();
        });
}

function removeUserFromGroup(userId) {
    let groupId = document.getElementById('addGroupMember').dataset.groupId;
    
    fetch(`/chat/remove_from_group/`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ user_id: userId, group_id: groupId })
    })
        .then(response => {
            location.reload();
        });
}

function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [name, value] = cookie.trim().split('=')
        if (name == 'csrftoken') {
            return value;
        }
    }
    return '';
}
