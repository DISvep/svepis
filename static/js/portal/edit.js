let editMode = false;
            
window.onload = () => {
    if (current_user == portal_user) {
        const widgets = document.querySelectorAll('.widget');
        
        document.getElementById('edit').addEventListener('click', editFunction);
        
        function editFunction() {
            if (editMode) {
                location.reload();
            } else {
                editMode = true;
                document.getElementById('edit').innerText = 'Save';
                widgets.forEach(widget => makeDraggable(widget));  
            }
        }
    }
}

function updatePosition(widgetId, x, y) {
    fetch(`/widget/update-widget-position/${widgetId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ x_position: x, y_position: y })
    });
}

function makeDraggable(widget) {
    let newX = 0, newY = 0, startX = 0, startY = 0, newTop = 0, newLeft = 0;
    
    const container = widget.parentElement;
    const containerRect = container.getBoundingClientRect();
    
    widget.addEventListener('mousedown', function (e) {
        startX = e.clientX
        startY = e.clientY
        
        document.addEventListener('mousemove', mouseMove)
        document.addEventListener('mouseup', mouseUp)
    });
    
    function mouseMove(e) {
        newX = startX - e.clientX
        newY = startY - e.clientY
        
        startX = e.clientX
        startY = e.clientY
        
        newTop = widget.offsetTop - newY;
        newLeft = widget.offsetLeft - newX;
        
        const widgetRect = widget.getBoundingClientRect();
        
        if (newLeft < 0) {
            newLeft = 0;
            console.log('LEFT');
        } else if (newLeft + widgetRect.width > containerRect.width) {
            newLeft = containerRect.width - widgetRect.width;
            console.log('RIGHT');
        }
        
        if (newTop < 0) {
            newTop = 0;
            console.log("TOP");
        } else if (newTop + widgetRect.height > 500) {
            newTop = 500 - widgetRect.height;
        }
        
        widget.style.top = newTop + 'px'
        widget.style.left = newLeft + 'px'
        
    }
    
    function mouseUp(e) {
        let x = parseInt(widget.style.left);
        let y = parseInt(widget.style.top);
        updatePosition(widget.dataset.id, x, y);
        document.removeEventListener('mousemove', mouseMove);
    }
    
}