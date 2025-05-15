function onClick(advert_id) {
    const button = event.currentTarget;
    const icon1 = button.querySelector('.icon1');
    const icon2 = button.querySelector('.icon2');

    fetch('/ajax/toggle-favourite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: new URLSearchParams({
            advert_id: advert_id,
            referer: window.location.pathname
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'unauthenticated') {
            window.location.href = data.login_url;
            return;
        }
        
        const icon1 = button.querySelector('.icon1');
        const icon2 = button.querySelector('.icon2');

        if (data.status === 'added') {
            icon1.style.display = 'flex';
            icon2.style.display = 'none';
        } else {
            icon1.style.display = 'none';
            icon2.style.display = 'flex';
        }
    })
    .catch(error => {
        console.error('Error toggling favorite:', error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}