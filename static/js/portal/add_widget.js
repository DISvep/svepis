document.addEventListener('DOMContentLoaded', function () {
    var select = document.getElementById('widgetType');
    select.selectedIndex = 0;
});

document.getElementById('widgetType').addEventListener("change", function () {
    var type = this.value;
    var contentField = document.getElementById('content');
    var imageField = document.getElementById('image');
    
    if (type === 'text') {
        contentField.style.display = "block";
    } else {
        contentField.style.display = "none";
    }
    
    if (type === "image") {
        imageField.style.display = "block";
    } else {
        imageField.style.display = "none";
    }
    
});