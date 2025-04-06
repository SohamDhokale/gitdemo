// Wishlist functionality for AaplaBazaar

document.addEventListener('DOMContentLoaded', function() {
    // Initialize wishlist forms with AJAX submission
    initWishlistForms();
});

// Initialize wishlist functionality
function initWishlistForms() {
    // Add to wishlist forms
    const addToWishlistForms = document.querySelectorAll('.add-to-wishlist-form');
    
    addToWishlistForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            submitFormAjax(form, 
                // Success callback
                function(data) {
                    showFlashMessage(data.message, 'success');
                    
                    // Update button or icon state
                    const wishlistBtn = form.querySelector('.wishlist-btn');
                    if (wishlistBtn) {
                        wishlistBtn.classList.add('active');
                        
                        // Replace icon if needed
                        const icon = wishlistBtn.querySelector('i');
                        if (icon && icon.classList.contains('far')) {
                            icon.classList.remove('far');
                            icon.classList.add('fas');
                        }
                    }
                },
                // Error callback
                function(data) {
                    showFlashMessage(data.message || 'Failed to add item to wishlist.', 'danger');
                }
            );
        });
    });
    
    // Remove from wishlist forms
    const removeWishlistForms = document.querySelectorAll('.remove-wishlist-form');
    
    removeWishlistForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            submitFormAjax(form, 
                // Success callback
                function(data) {
                    showFlashMessage(data.message, 'success');
                    
                    // Remove item from DOM if on wishlist page
                    const wishlistItem = form.closest('.wishlist-item');
                    if (wishlistItem) {
                        wishlistItem.classList.add('fade-out');
                        setTimeout(() => {
                            wishlistItem.remove();
                            
                            // Check if wishlist is empty now
                            const remainingItems = document.querySelectorAll('.wishlist-item');
                            if (remainingItems.length === 0) {
                                showEmptyWishlist();
                            }
                        }, 300);
                    }
                    
                    // Update button state if on product page
                    const wishlistBtn = document.querySelector(`.wishlist-btn[data-product-id="${form.querySelector('input[name="product_id"]').value}"]`);
                    if (wishlistBtn) {
                        wishlistBtn.classList.remove('active');
                        
                        // Replace icon if needed
                        const icon = wishlistBtn.querySelector('i');
                        if (icon && icon.classList.contains('fas')) {
                            icon.classList.remove('fas');
                            icon.classList.add('far');
                        }
                    }
                },
                // Error callback
                function(data) {
                    showFlashMessage(data.message || 'Failed to remove item from wishlist.', 'danger');
                }
            );
        });
    });
    
    // Toggle wishlist buttons (for product cards)
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Find the correct form to submit
            const productId = this.getAttribute('data-product-id');
            let form;
            
            if (this.classList.contains('active')) {
                // Find remove form
                form = document.querySelector(`.remove-wishlist-form input[value="${productId}"]`);
                if (form) form = form.closest('form');
            } else {
                // Find add form
                form = document.querySelector(`.add-to-wishlist-form input[value="${productId}"]`);
                if (form) form = form.closest('form');
            }
            
            if (form) {
                const submitEvent = new Event('submit', { cancelable: true });
                form.dispatchEvent(submitEvent);
            }
        });
    });
}

// Show empty wishlist message
function showEmptyWishlist() {
    const wishlistContainer = document.querySelector('.wishlist-items');
    
    if (wishlistContainer) {
        // Create empty wishlist message
        const emptyWishlistMessage = document.createElement('div');
        emptyWishlistMessage.classList.add('empty-wishlist-message', 'text-center', 'py-5');
        
        emptyWishlistMessage.innerHTML = `
            <i class="far fa-heart fa-3x mb-3"></i>
            <h3>Your wishlist is empty</h3>
            <p>Add items you love to your wishlist.</p>
            <a href="/products" class="btn btn-primary mt-3">Browse Products</a>
        `;
        
        wishlistContainer.innerHTML = '';
        wishlistContainer.appendChild(emptyWishlistMessage);
    }
}
