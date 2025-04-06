// Cart functionality for AaplaBazaar

document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart forms with AJAX submission
    initCartForms();
    
    // Set up checkout button events
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            window.location.href = '/checkout';
        });
    }
    
    // Update cart totals if on cart page
    updateCartTotals();
});

// Initialize cart functionality
function initCartForms() {
    // Add to cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            submitFormAjax(form, 
                // Success callback
                function(data) {
                    showFlashMessage(data.message, 'success');
                    
                    // Get current cart count and update
                    const cartBadge = document.querySelector('.badge-cart');
                    if (cartBadge) {
                        const currentCount = parseInt(cartBadge.textContent) || 0;
                        updateCartCount(currentCount + 1);
                    }
                },
                // Error callback
                function(data) {
                    showFlashMessage(data.message || 'Failed to add item to cart.', 'danger');
                }
            );
        });
    });
    
    // Update cart item forms
    const updateCartForms = document.querySelectorAll('.update-cart-form');
    
    updateCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            submitFormAjax(form, 
                // Success callback
                function(data) {
                    // Update cart counts and totals
                    updateCartCount(data.itemCount);
                    updateCartTotals(data.total);
                    
                    // Check if item was removed
                    const quantity = parseInt(form.querySelector('.quantity-input').value);
                    if (quantity <= 0) {
                        const cartItem = form.closest('.cart-item');
                        if (cartItem) {
                            cartItem.classList.add('fade-out');
                            setTimeout(() => {
                                cartItem.remove();
                                
                                // Check if cart is empty now
                                const remainingItems = document.querySelectorAll('.cart-item');
                                if (remainingItems.length === 0) {
                                    showEmptyCart();
                                }
                            }, 300);
                        }
                    }
                },
                // Error callback
                function(data) {
                    showFlashMessage(data.message || 'Failed to update cart.', 'danger');
                }
            );
        });
    });
    
    // Remove from cart forms
    const removeCartForms = document.querySelectorAll('.remove-cart-form');
    
    removeCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            submitFormAjax(form, 
                // Success callback
                function(data) {
                    showFlashMessage(data.message, 'success');
                    
                    // Update cart count
                    updateCartCount(data.itemCount);
                    
                    // Remove item from DOM
                    const cartItem = form.closest('.cart-item');
                    if (cartItem) {
                        cartItem.classList.add('fade-out');
                        setTimeout(() => {
                            cartItem.remove();
                            
                            // Update totals
                            updateCartTotals(data.total);
                            
                            // Check if cart is empty now
                            const remainingItems = document.querySelectorAll('.cart-item');
                            if (remainingItems.length === 0) {
                                showEmptyCart();
                            }
                        }, 300);
                    }
                },
                // Error callback
                function(data) {
                    showFlashMessage(data.message || 'Failed to remove item from cart.', 'danger');
                }
            );
        });
    });
}

// Update cart totals
function updateCartTotals(newTotal) {
    const totalElement = document.querySelector('.cart-total-value');
    
    if (totalElement) {
        if (newTotal !== undefined) {
            // Format as Indian Rupees
            totalElement.textContent = '₹' + parseFloat(newTotal).toFixed(2);
        } else {
            // Calculate from DOM
            let total = 0;
            const cartItems = document.querySelectorAll('.cart-item');
            
            cartItems.forEach(item => {
                const price = parseFloat(item.querySelector('.cart-item-price').getAttribute('data-price'));
                const quantity = parseInt(item.querySelector('.quantity-input').value);
                total += price * quantity;
            });
            
            totalElement.textContent = '₹' + total.toFixed(2);
        }
    }
}

// Show empty cart message
function showEmptyCart() {
    const cartContainer = document.querySelector('.cart-items');
    const cartSummary = document.querySelector('.cart-summary');
    
    if (cartContainer) {
        // Create empty cart message
        const emptyCartMessage = document.createElement('div');
        emptyCartMessage.classList.add('empty-cart-message', 'text-center', 'py-5');
        
        emptyCartMessage.innerHTML = `
            <i class="fas fa-shopping-cart fa-3x mb-3"></i>
            <h3>Your cart is empty</h3>
            <p>Looks like you haven't added anything to your cart yet.</p>
            <a href="/products" class="btn btn-primary mt-3">Browse Products</a>
        `;
        
        cartContainer.innerHTML = '';
        cartContainer.appendChild(emptyCartMessage);
        
        // Hide the summary and checkout button
        if (cartSummary) {
            cartSummary.style.display = 'none';
        }
    }
}
