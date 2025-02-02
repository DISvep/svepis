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
