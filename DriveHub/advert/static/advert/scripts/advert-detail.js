let slideIndex = 0;

function showSlides(n) {
    let images = document.getElementsByClassName("bottom-image");
    let mainImage = document.querySelector(".main-image");
    console.log(slideIndex);

    if (n > images.length - 1) {
        slideIndex = 0;
    }
    else if (n < 0) {
        slideIndex = images.length - 1;
    }

    mainImage.src = images[slideIndex].src; 

}

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

const row = document.querySelector(".image-preview-row");

row.addEventListener('wheel', function(e) {
    if (e.deltaY !== 0) {
        e.preventDefault();
        row.scrollLeft += e.deltaY;
    }
}, { passive: false });



function toggleFavourite(advertId) {
    const button = document.querySelector(".favourite-button-container");
    fetch('/ajax/toggle-favourite/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: new URLSearchParams({
            advert_id: advertId,
            referer: window.location.pathname
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'unauthenticated') {
            window.location.href = data.login_url;
            return;
        }
        
        const redIcon = button.querySelector('.red-icon');
        const blackIcon = button.querySelector('.black-icon');

        if (data.status === 'added') {
            redIcon.style.display = 'flex';
            blackIcon.style.display = 'none';
        } else {
            redIcon.style.display = 'none';
            blackIcon.style.display = 'flex';
        }
    })
    .catch(error => {
        console.error('Error toggling favorite:', error);
    });
}

// CSRF helper
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}