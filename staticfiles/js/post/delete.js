$("#deleteModal").on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const username = button.getAttribute("data-username");
    const date = button.getAttribute("data-date");
    const pk = button.getAttribute("data-pk");
    
    const deleteLabel = document.getElementById("deleteModalLabel");
    deleteLabel.textContent = `Delete post by @${username} at ${date}?`
    
    const deleteForm = document.getElementById("deleteForm");
    deleteForm.action = `/post/delete/${pk}`;
});