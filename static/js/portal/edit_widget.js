document.getElementById("deleteWidgetButton").addEventListener("click", function () {
    var select = document.getElementById('widgetChoice');
    var widget_id = select.options[select.selectedIndex].value;
    var form = document.getElementById('deleteWidgetForm');
    form.action = `/widget/delete-widget/${widget_id}`;
});

document.getElementById("editSaveButton").addEventListener("click", function () {
    var select = document.getElementById('widgetChoice');
    var widget_id = select.options[select.selectedIndex].value;
    var width = document.getElementById('width').value;
    var height = document.getElementById('height').value;
    var z_index = document.getElementById('z-index').value;
    fetch(`/widget/update-widget/${widget_id}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ width: width, height: height, z_index: z_index })
    }).then(function () {
        location.reload();
    });
});