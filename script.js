// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Project card click handlers
document.querySelectorAll('.project-card.clickable').forEach(card => {
    card.addEventListener('click', function() {
        // Check if it's a certificate card
        if (this.classList.contains('certificate-card')) {
            const certUrl = this.getAttribute('data-cert-url');
            if (certUrl) {
                window.open(certUrl, '_blank');
            }
        } else {
            // Regular project page
            const projectName = this.getAttribute('data-project');
            window.location.href = `projects/${projectName}.html`;
        }
    });
});

// Fade in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Header background change on scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
    }
});

// Photo Slider for C2C page
document.addEventListener('DOMContentLoaded', function () {
    const track = document.getElementById('sliderTrack');
    const dots = document.querySelectorAll('.slider-dot');
    const totalSlides = document.querySelectorAll('.slider-slide').length;
    let currentSlideIndex = 0;

    function showSlide(index) {
        if (index >= totalSlides) {
            currentSlideIndex = 0;
        } else if (index < 0) {
            currentSlideIndex = totalSlides - 1;
        } else {
            currentSlideIndex = index;
        }
        const translateX = -currentSlideIndex * (100 / totalSlides);
        track.style.transform = `translateX(${translateX}%)`;
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlideIndex);
        });
    }

    window.changeSlide = function (direction) {
        showSlide(currentSlideIndex + direction);
    };

    window.currentSlide = function (index) {
        showSlide(index - 1);
    };

    showSlide(0);

    // Touch/swipe support
    let startX = 0, startY = 0;
    const sliderContainer = document.querySelector('.slider-container');
    if (sliderContainer) {
        sliderContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });
        sliderContainer.addEventListener('touchend', (e) => {
            if (!startX || !startY) return;
            const endX = e.changedTouches[0].clientX;
            const endY = e.changedTouches[0].clientY;
            const diffX = startX - endX;
            const diffY = startY - endY;
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                if (diffX > 0) changeSlide(1);
                else changeSlide(-1);
            }
            startX = 0; startY = 0;
        });
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') changeSlide(-1);
        else if (e.key === 'ArrowRight') changeSlide(1);
    });

    // Optional: Auto-play
    // setInterval(() => { changeSlide(1); }, 5000);
});