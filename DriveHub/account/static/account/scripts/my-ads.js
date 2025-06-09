function onClick(advertId) {
    fetch(`/delete/${advertId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
        }
    })
    .then(response => {
        if (response.redirected || response.ok) {
            location.reload();
        } else {
            throw new Error("Помилка HTTP");
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