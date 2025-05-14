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