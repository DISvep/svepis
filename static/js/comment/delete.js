$("#deleteCommentModal").on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const username = button.getAttribute("data-username");
    const date = button.getAttribute("data-date");
    const pk = button.getAttribute("data-pk");
    
    const deleteLabel = document.getElementById("deleteCommentModalLabel");
    deleteLabel.textContent = `Delete comment by @${username} at ${date}?`
    
    const deleteForm = document.getElementById("deleteCommentForm");
    deleteForm.action = `/comment/${pk}/delete`;
});