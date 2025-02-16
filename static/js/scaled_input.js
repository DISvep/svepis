textarea.addEventListener('input', function(){
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
    submit.style.display = 'block';
    cancel.style.display = 'block';
});

function resetComment(){
    textarea.value = "";
    textarea.style.height = 'auto';
    submit.style.display = 'none';
    cancel.style.display = 'none';
};