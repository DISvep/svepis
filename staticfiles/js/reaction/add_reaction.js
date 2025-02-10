document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-reaction-btn').forEach((button) => {   
        const pk = button.dataset.pk;
        const pickerContainer = document.querySelector(`.emoji-picker-container[data-pk="${pk}"]`);
        
        if (!pickerContainer) return;
        
        const picker = new EmojiMart.Picker({ onEmojiSelect: (emoji) => handleEmojiSelect(pk, emoji) });
        pickerContainer.appendChild(picker);
        pickerContainer.style.display = "none";
        
        button.addEventListener("click", () => {
            pickerContainer.style.display = pickerContainer.style.display === "none" ? "block" : "none";
        });
    });
});

function handleEmojiSelect(pk, emoji) {
    const pickerContainer = document.querySelector(`.emoji-picker-container[data-pk="${pk}"]`);
    if (pickerContainer) pickerContainer.style.display = "none";
    
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/reaction/post/${pk}`;
    form.style.display = 'none';
    
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = getCookie('csrftoken');
    form.appendChild(csrfInput);
    
    const emojiInput = document.createElement('input');
    emojiInput.type = 'hidden';
    emojiInput.name = 'emoji';
    emojiInput.value = emoji.native;
    form.appendChild(emojiInput);
    
    document.body.appendChild(form);
    form.submit();
}
    
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}