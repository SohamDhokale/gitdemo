// Main JavaScript file for AaplaBazaar

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeSlider();
    initializeNavbar();
    initializeProductImages();
    initializeQuantityButtons();
    initializeImageGallery();
    initializeTooltips();
    
    // Flash messages auto-dismiss
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.alert');
        flashMessages.forEach(function(message) {
            message.classList.add('fade-out');
            setTimeout(function() {
                message.remove();
            }, 500); // Match this with the CSS transition time
        });
    }, 5000); // 5 seconds auto-dismiss
});

// Navigation bar scroll behavior
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }
}

// Initialize home page slider
function initializeSlider() {
    const heroSlider = document.querySelector('.hero-slider-container');
    
    if (heroSlider) {
        new Swiper('.hero-slider-container', {
            slidesPerView: 1,
            spaceBetween: 0,
            loop: true,
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
        });
    }
}

// Product thumbnail gallery
function initializeProductImages() {
    const productThumbnails = document.querySelectorAll('.product-thumbnail');
    const mainImage = document.querySelector('.product-main-image img');
    
    if (productThumbnails.length && mainImage) {
        productThumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Update main image
                const imgSrc = this.querySelector('img').getAttribute('src');
                mainImage.setAttribute('src', imgSrc);
                
                // Update active class
                productThumbnails.forEach(thumb => thumb.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

// Initialize quantity buttons
function initializeQuantityButtons() {
    const decrementButtons = document.querySelectorAll('.quantity-decrement');
    const incrementButtons = document.querySelectorAll('.quantity-increment');
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    // Decrement button functionality
    decrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('.quantity-input');
            let value = parseInt(input.value);
            value = value > 1 ? value - 1 : 1;
            input.value = value;
            
            // If in cart page, trigger update
            if (this.closest('.cart-item')) {
                const updateForm = this.closest('form');
                if (updateForm) {
                    const event = new Event('submit', { cancelable: true });
                    updateForm.dispatchEvent(event);
                }
            }
        });
    });
    
    // Increment button functionality
    incrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentNode.querySelector('.quantity-input');
            let value = parseInt(input.value);
            const max = input.hasAttribute('max') ? parseInt(input.getAttribute('max')) : 99;
            value = value < max ? value + 1 : max;
            input.value = value;
            
            // If in cart page, trigger update
            if (this.closest('.cart-item')) {
                const updateForm = this.closest('form');
                if (updateForm) {
                    const event = new Event('submit', { cancelable: true });
                    updateForm.dispatchEvent(event);
                }
            }
        });
    });
    
    // Ensure quantity inputs only accept numbers
    quantityInputs.forEach(input => {
        input.addEventListener('input', function() {
            const value = parseInt(this.value);
            const min = parseInt(this.getAttribute('min') || 1);
            const max = parseInt(this.getAttribute('max') || 99);
            
            if (isNaN(value) || value < min) {
                this.value = min;
            } else if (value > max) {
                this.value = max;
            }
        });
        
        // Update cart on change
        input.addEventListener('change', function() {
            if (this.closest('.cart-item')) {
                const updateForm = this.closest('form');
                if (updateForm) {
                    const event = new Event('submit', { cancelable: true });
                    updateForm.dispatchEvent(event);
                }
            }
        });
    });
}

// Image gallery lightbox for product pages
function initializeImageGallery() {
    const productImages = document.querySelectorAll('.product-main-image, .product-thumbnail');
    
    if (productImages.length) {
        productImages.forEach(image => {
            image.addEventListener('click', function() {
                if (this.classList.contains('product-main-image')) {
                    const imgSrc = this.querySelector('img').getAttribute('src');
                    openLightbox(imgSrc);
                }
            });
        });
    }
}

// Lightbox functionality
function openLightbox(imgSrc) {
    // Create lightbox elements
    const lightbox = document.createElement('div');
    lightbox.classList.add('lightbox');
    
    const img = document.createElement('img');
    img.setAttribute('src', imgSrc);
    
    const closeBtn = document.createElement('span');
    closeBtn.classList.add('lightbox-close');
    closeBtn.innerHTML = '&times;';
    
    // Append elements
    lightbox.appendChild(closeBtn);
    lightbox.appendChild(img);
    document.body.appendChild(lightbox);
    
    // Prevent body scrolling
    document.body.style.overflow = 'hidden';
    
    // Close functionality
    closeBtn.addEventListener('click', function() {
        closeLightbox(lightbox);
    });
    
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            closeLightbox(lightbox);
        }
    });
    
    // Close on ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox(lightbox);
        }
    });
}

function closeLightbox(lightbox) {
    lightbox.classList.add('fade-out');
    setTimeout(function() {
        document.body.removeChild(lightbox);
        document.body.style.overflow = '';
    }, 300);
}

// Initialize tooltips
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
    
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const title = this.getAttribute('title') || this.getAttribute('data-original-title');
            
            if (!title) return;
            
            // Create tooltip
            const tooltipElement = document.createElement('div');
            tooltipElement.classList.add('tooltip');
            tooltipElement.textContent = title;
            
            // Position tooltop
            document.body.appendChild(tooltipElement);
            
            const rect = this.getBoundingClientRect();
            const tooltipRect = tooltipElement.getBoundingClientRect();
            
            tooltipElement.style.top = rect.top - tooltipRect.height - 10 + 'px';
            tooltipElement.style.left = rect.left + (rect.width / 2) - (tooltipRect.width / 2) + 'px';
            
            tooltipElement.classList.add('show');
            
            // Store reference
            this.tooltipElement = tooltipElement;
            
            // Remove title to prevent default tooltip
            this.setAttribute('data-original-title', title);
            this.removeAttribute('title');
        });
        
        tooltip.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.classList.remove('show');
                setTimeout(() => {
                    document.body.removeChild(this.tooltipElement);
                    delete this.tooltipElement;
                }, 300);
                
                // Restore title
                const originalTitle = this.getAttribute('data-original-title');
                if (originalTitle) {
                    this.setAttribute('title', originalTitle);
                    this.removeAttribute('data-original-title');
                }
            }
        });
    });
}

// AJAX form submission
function submitFormAjax(form, successCallback, errorCallback) {
    const formData = new FormData(form);
    const url = form.getAttribute('action');
    const method = form.getAttribute('method') || 'POST';
    
    fetch(url, {
        method: method,
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (successCallback) successCallback(data);
        } else {
            if (errorCallback) errorCallback(data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (errorCallback) errorCallback({ success: false, message: 'An error occurred while processing your request.' });
    });
}

// Show flash message
function showFlashMessage(message, type) {
    let flashContainer = document.querySelector('.flash-container');
    
    if (!flashContainer) {
        flashContainer = document.createElement('div');
        flashContainer.classList.add('flash-container');
        const mainContent = document.querySelector('main') || document.body;
        mainContent.insertBefore(flashContainer, mainContent.firstChild);
    }
    
    const flashMessage = document.createElement('div');
    flashMessage.classList.add('alert', `alert-${type || 'info'}`);
    flashMessage.textContent = message;
    
    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.classList.add('close');
    closeButton.innerHTML = '&times;';
    closeButton.addEventListener('click', function() {
        flashMessage.remove();
    });
    
    flashMessage.appendChild(closeButton);
    flashContainer.appendChild(flashMessage);
    
    // Auto-dismiss
    setTimeout(function() {
        flashMessage.classList.add('fade-out');
        setTimeout(function() {
            flashMessage.remove();
        }, 500);
    }, 5000);
}

// Update cart count in navbar
function updateCartCount(count) {
    const cartBadge = document.querySelector('.badge-cart');
    if (cartBadge) {
        cartBadge.textContent = count;
        
        if (count <= 0) {
            cartBadge.style.display = 'none';
        } else {
            cartBadge.style.display = 'block';
        }
    }
}
