let offset = 0;
        
function loadMore() {
    fetch(`/load-more-announcements/?offset=${offset}`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('announcements');
            data.announcements.forEach(item => {
                announcementCard = document.getElementById(`announcement_${item.pk}`);
                announcementCard.style.display = "block";
            });

            offset += 1;

            if (data.announcements.length < 1) {
                document.getElementById('load-more').style.display = 'none';
            }
        });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('load-more').addEventListener('click', loadMore);
});