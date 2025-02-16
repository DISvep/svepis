$('#updateModal').on('show.bs.modal', function (event) {
    const updateForm = document.getElementById("updateForm");
    const button = event.relatedTarget;
    const area = document.getElementById("areaUpdate");
    
    const pk = button.getAttribute('data-pk');
    const content = button.getAttribute('data-content');
    
    area.value = content;
    updateForm.action = `/comment/${pk}/update`;
});