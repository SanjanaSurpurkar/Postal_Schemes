const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const slider = document.querySelector('.slider');
let index = 0;
const slides = document.querySelectorAll('.slide');
const slideCount = slides.length;
const intervalTime = 3000; // Time in milliseconds (3000ms = 3 seconds)

// Function to show a specific slide
function showSlide(n) {
    if (n >= slideCount) index = 0;
    if (n < 0) index = slideCount - 1;
    slider.style.transform = `translateX(${-index * 100}%)`;
}

// Function to go to the next slide
function nextSlide() {
    index++;
    showSlide(index);
}

// Set up the interval to automatically go to the next slide
const slideInterval = setInterval(nextSlide, intervalTime);

// Event listeners for the navigation buttons
prevBtn.addEventListener('click', () => {
    index--;
    showSlide(index);
    resetInterval();
});

nextBtn.addEventListener('click', () => {
    index++;
    showSlide(index);
    resetInterval();
});

// Reset the interval when a manual change is made
function resetInterval() {
    clearInterval(slideInterval);
    setInterval(nextSlide, intervalTime);
}

// Initial slide setup
showSlide(index);
