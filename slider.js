// Image slider functionality for AaplaBazaar

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the hero slider (home page)
    initHeroSlider();
    
    // Initialize product gallery slider
    initProductGallery();
});

// Initialize the main hero slider on the home page
function initHeroSlider() {
    const heroSlider = document.querySelector('.hero-slider');
    
    if (heroSlider) {
        new Swiper('.hero-slider', {
            slidesPerView: 1,
            spaceBetween: 0,
            loop: true,
            speed: 800,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            },
            keyboard: {
                enabled: true,
                onlyInViewport: true,
            },
        });
    }
}

// Initialize product gallery slider
function initProductGallery() {
    const productThumbnails = document.querySelector('.product-thumbnails');
    
    if (productThumbnails) {
        // Set up click handling for thumbnails
        const thumbnails = productThumbnails.querySelectorAll('.product-thumbnail');
        const mainImage = document.querySelector('.product-main-image img');
        
        if (thumbnails.length && mainImage) {
            thumbnails.forEach(thumbnail => {
                thumbnail.addEventListener('click', function() {
                    // Remove active class from all thumbnails
                    thumbnails.forEach(t => t.classList.remove('active'));
                    
                    // Add active class to clicked thumbnail
                    this.classList.add('active');
                    
                    // Update main image
                    const newSrc = this.querySelector('img').getAttribute('src');
                    
                    // Fade transition effect
                    mainImage.style.opacity = '0';
                    setTimeout(() => {
                        mainImage.setAttribute('src', newSrc);
                        mainImage.style.opacity = '1';
                    }, 300);
                });
            });
            
            // Set first thumbnail as active by default
            if (thumbnails.length > 0 && !document.querySelector('.product-thumbnail.active')) {
                thumbnails[0].classList.add('active');
            }
        }
    }
    
    // Initialize category product sliders if present
    const categorySliders = document.querySelectorAll('.category-products-slider');
    
    if (categorySliders.length) {
        categorySliders.forEach(slider => {
            new Swiper(slider, {
                slidesPerView: 1,
                spaceBetween: 20,
                navigation: {
                    nextEl: slider.querySelector('.swiper-button-next'),
                    prevEl: slider.querySelector('.swiper-button-prev'),
                },
                breakpoints: {
                    576: {
                        slidesPerView: 2,
                        spaceBetween: 20,
                    },
                    768: {
                        slidesPerView: 3,
                        spaceBetween: 30,
                    },
                    992: {
                        slidesPerView: 4,
                        spaceBetween: 30,
                    },
                },
            });
        });
    }
    
    // Initialize related products slider if present
    const relatedSlider = document.querySelector('.related-products-slider');
    
    if (relatedSlider) {
        new Swiper(relatedSlider, {
            slidesPerView: 1,
            spaceBetween: 20,
            navigation: {
                nextEl: '.related-products-next',
                prevEl: '.related-products-prev',
            },
            breakpoints: {
                576: {
                    slidesPerView: 2,
                    spaceBetween: 20,
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 30,
                },
                992: {
                    slidesPerView: 4,
                    spaceBetween: 30,
                },
            },
        });
    }
}
