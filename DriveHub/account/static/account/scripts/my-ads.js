function onClick(advertId) {
    fetch(`/delete/${advertId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    })
    .catch(error => {
        alert("Не вдалося видалити оголошення.");
        console.error(error);
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}