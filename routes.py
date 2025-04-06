import os
import logging
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, jsonify, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash

from app import app, db
from models import User, Product, Order, OrderItem, CartItem, WishlistItem, OrderTracking, Review
from forms import LoginForm, RegistrationForm, ProductForm, CheckoutForm, ReviewForm
from utils import send_sms_notification, generate_order_tracking

# Home page
@app.route('/')
def index():
    featured_products = Product.query.filter_by(is_featured=True).limit(8).all()
    gi_tagged_products = Product.query.filter_by(is_gi_tagged=True).limit(4).all()
    
    # Get categories for filter
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]
    
    return render_template('index.html', 
                           featured_products=featured_products,
                           gi_tagged_products=gi_tagged_products,
                           categories=categories,
                           title='AaplaBazaar - Indian E-Commerce Platform')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        
        flash('Login successful!', 'success')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now registered! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Product routes
@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    sort = request.args.get('sort', 'newest')
    search = request.args.get('search', '')
    
    # Base query
    query = Product.query
    
    # Apply filters
    if category and category != 'all':
        query = query.filter_by(category=category)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%') | 
                             Product.description.ilike(f'%{search}%'))
    
    # Apply sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    
    # Pagination
    products = query.paginate(page=page, per_page=12, error_out=False)
    
    # Get categories for filter
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]
    
    return render_template('products.html', 
                           title='Products',
                           products=products,
                           categories=categories,
                           current_category=category,
                           current_sort=sort,
                           search=search)

@app.route('/product/<int:id>', methods=['GET', 'POST'])
def product_detail(id):
    product = Product.query.get_or_404(id)
    # Get related products from the same category
    related_products = Product.query.filter_by(category=product.category).filter(Product.id != id).limit(4).all()
    
    # Get reviews for the product
    reviews = Review.query.filter_by(product_id=id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    
    # Initialize review form
    form = None
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            # Check if user has already reviewed the product
            existing_review = Review.query.filter_by(user_id=current_user.id, product_id=id).first()
            
            if existing_review:
                # Update existing review
                existing_review.rating = int(form.rating.data)
                existing_review.title = form.title.data
                existing_review.comment = form.comment.data
                existing_review.updated_at = datetime.utcnow()
                flash('Your review has been updated!', 'success')
            else:
                # Create new review
                review = Review(
                    user_id=current_user.id,
                    product_id=id,
                    rating=int(form.rating.data),
                    title=form.title.data,
                    comment=form.comment.data
                )
                db.session.add(review)
                flash('Thank you for your review!', 'success')
            
            db.session.commit()
            return redirect(url_for('product_detail', id=id))
    
    return render_template('product_detail.html', 
                          title=product.name,
                          product=product,
                          related_products=related_products,
                          reviews=reviews,
                          avg_rating=avg_rating,
                          form=form)

# Cart routes
@app.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', 
                           title='Your Cart',
                           cart_items=cart_items,
                           total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if item is already in cart
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    quantity = int(request.form.get('quantity', 1))
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    flash(f'{product.name} added to your cart!', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return jsonify({'success': True, 'message': f'{product.name} added to your cart!'})
    
    return redirect(url_for('product_detail', id=product_id))

@app.route('/update_cart_item/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify that the item belongs to the current user
    if cart_item.user_id != current_user.id:
        abort(403)
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        message = f'{cart_item.product.name} removed from your cart!'
    else:
        cart_item.quantity = quantity
        message = f'Cart updated!'
    
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        return jsonify({
            'success': True, 
            'message': message,
            'total': total,
            'itemCount': len(cart_items)
        })
    
    flash(message, 'success')
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verify that the item belongs to the current user
    if cart_item.user_id != current_user.id:
        abort(403)
    
    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()
    
    flash(f'{product_name} removed from your cart!', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
        return jsonify({
            'success': True, 
            'message': f'{product_name} removed from your cart!',
            'total': total,
            'itemCount': len(cart_items)
        })
    
    return redirect(url_for('cart'))

# Wishlist routes
@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    
    return render_template('wishlist.html', 
                           title='Your Wishlist',
                           wishlist_items=wishlist_items)

@app.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if item is already in wishlist
    wishlist_item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if wishlist_item:
        flash(f'{product.name} is already in your wishlist!', 'info')
    else:
        wishlist_item = WishlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash(f'{product.name} added to your wishlist!', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return jsonify({'success': True, 'message': f'{product.name} added to your wishlist!'})
    
    return redirect(url_for('product_detail', id=product_id))

@app.route('/remove_from_wishlist/<int:item_id>', methods=['POST'])
@login_required
def remove_from_wishlist(item_id):
    wishlist_item = WishlistItem.query.get_or_404(item_id)
    
    # Verify that the item belongs to the current user
    if wishlist_item.user_id != current_user.id:
        abort(403)
    
    product_name = wishlist_item.product.name
    db.session.delete(wishlist_item)
    db.session.commit()
    
    flash(f'{product_name} removed from your wishlist!', 'success')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return jsonify({
            'success': True, 
            'message': f'{product_name} removed from your wishlist!'
        })
    
    return redirect(url_for('wishlist'))

# Checkout and order routes
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty. Add some products first.', 'info')
        return redirect(url_for('products'))
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    form = CheckoutForm()
    # Pre-fill address if user has one
    if request.method == 'GET' and current_user.address:
        form.shipping_address.data = current_user.address
        form.shipping_city.data = current_user.city
        form.shipping_state.data = current_user.state
        form.shipping_pincode.data = current_user.pincode
    
    if form.validate_on_submit():
        # Create the order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=form.shipping_address.data,
            shipping_city=form.shipping_city.data,
            shipping_state=form.shipping_state.data,
            shipping_pincode=form.shipping_pincode.data,
            status='Processing',
            payment_status='Pending'  # For Cash on Delivery
        )
        db.session.add(order)
        db.session.flush()  # Get the order ID
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            db.session.add(order_item)
        
        # Generate a tracking number
        order.tracking_number = f'AAPLA{order.id}{datetime.utcnow().strftime("%Y%m%d%H%M")}'
        
        # Generate estimated delivery date and tracking updates
        tracking_updates, estimated_delivery = generate_order_tracking(order)
        order.estimated_delivery = estimated_delivery
        
        # Add tracking information
        for update in tracking_updates:
            tracking = OrderTracking(
                order_id=order.id,
                status=update['status'],
                location=update['location'],
                timestamp=update['timestamp'],
                description=update['description']
            )
            db.session.add(tracking)
        
        # Clear the user's cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        # Commit all changes
        db.session.commit()
        
        # Send SMS notification
        message = f"Thank you for shopping with AaplaBazaar! Your order #{order.id} has been confirmed. Track your order with ID: {order.tracking_number}"
        send_result = send_sms_notification(current_user.phone, message)
        
        if send_result:
            app.logger.info(f"SMS notification sent successfully for order {order.id}")
        else:
            app.logger.warning(f"Failed to send SMS notification for order {order.id}")
        
        flash('Your order has been placed successfully! You will receive an SMS with tracking details.', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    return render_template('checkout.html', 
                           title='Checkout',
                           cart_items=cart_items,
                           total=total,
                           form=form)



@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Verify that the order belongs to the current user
    if order.user_id != current_user.id:
        abort(403)
    
    return render_template('order_confirmation.html',
                           title='Order Confirmation',
                           order=order)

@app.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.order_date.desc()).all()
    
    return render_template('orders.html',
                           title='Your Orders',
                           orders=orders)

@app.route('/order/track/<int:order_id>')
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Verify that the order belongs to the current user
    if order.user_id != current_user.id:
        abort(403)
    
    # Get tracking updates
    tracking_updates = OrderTracking.query.filter_by(order_id=order.id).order_by(OrderTracking.timestamp.asc()).all()
    
    return render_template('order_tracking.html',
                           title='Track Order',
                           order=order,
                           tracking_updates=tracking_updates)

# Profile routes
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Your Profile')

@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = RegistrationForm()
    
    # Remove the validation of username and email
    delattr(form, 'validate_username')
    delattr(form, 'validate_email')
    
    # Pre-fill the form with current user data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.pincode.data = current_user.pincode
    
    if form.validate_on_submit():
        # Check if username or email has changed
        username_changed = current_user.username != form.username.data
        email_changed = current_user.email != form.email.data
        
        if username_changed:
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken. Please choose another one.', 'danger')
                return redirect(url_for('update_profile'))
        
        if email_changed:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already in use. Please choose another one.', 'danger')
                return redirect(url_for('update_profile'))
        
        # Update user data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.pincode = form.pincode.data
        
        # Update password if provided
        if form.password.data:
            current_user.set_password(form.password.data)
        
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))
    
    return render_template('update_profile.html', title='Update Profile', form=form)

# Review routes
@app.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    # Verify that the review belongs to the current user or user is admin
    if review.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    product_id = review.product_id
    db.session.delete(review)
    db.session.commit()
    
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('product_detail', id=product_id))

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    product_count = Product.query.count()
    user_count = User.query.count()
    order_count = Order.query.count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                           title='Admin Dashboard',
                           product_count=product_count,
                           user_count=user_count,
                           order_count=order_count,
                           recent_orders=recent_orders)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    products = Product.query.all()
    
    return render_template('admin/manage_products.html',
                           title='Manage Products',
                           products=products)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    form = ProductForm()
    
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            discount_price=form.discount_price.data,
            stock=form.stock.data,
            category=form.category.data,
            image_url1=form.image_url1.data,
            image_url2=form.image_url2.data,
            image_url3=form.image_url3.data,
            is_featured=form.is_featured.data,
            is_gi_tagged=form.is_gi_tagged.data,
            gi_tag_details=form.gi_tag_details.data,
            origin=form.origin.data
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{product.name}" has been added!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html',
                           title='Add Product',
                           form=form)

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    form = ProductForm()
    
    # Pre-fill the form with product data
    if request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.discount_price.data = product.discount_price
        form.stock.data = product.stock
        form.category.data = product.category
        form.image_url1.data = product.image_url1
        form.image_url2.data = product.image_url2
        form.image_url3.data = product.image_url3
        form.is_featured.data = product.is_featured
        form.is_gi_tagged.data = product.is_gi_tagged
        form.gi_tag_details.data = product.gi_tag_details
        form.origin.data = product.origin
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.discount_price = form.discount_price.data
        product.stock = form.stock.data
        product.category = form.category.data
        product.image_url1 = form.image_url1.data
        product.image_url2 = form.image_url2.data
        product.image_url3 = form.image_url3.data
        product.is_featured = form.is_featured.data
        product.is_gi_tagged = form.is_gi_tagged.data
        product.gi_tag_details = form.gi_tag_details.data
        product.origin = form.origin.data
        
        db.session.commit()
        
        flash(f'Product "{product.name}" has been updated!', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html',
                           title='Edit Product',
                           form=form,
                           product=product)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    flash(f'Product "{product.name}" has been deleted!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.order_date.desc()).all()
    
    return render_template('admin/manage_orders.html',
                           title='Manage Orders',
                           orders=orders)

@app.route('/admin/order/<int:order_id>')
@login_required
def admin_order_detail(order_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    tracking_updates = OrderTracking.query.filter_by(order_id=order.id).order_by(OrderTracking.timestamp.asc()).all()
    
    return render_template('admin/order_detail.html',
                           title='Order Detail',
                           order=order,
                           user=user,
                           tracking_updates=tracking_updates)

@app.route('/admin/order/update/<int:order_id>', methods=['POST'])
@login_required
def admin_update_order(order_id):
    if not current_user.is_admin:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    
    if status:
        order.status = status
        db.session.commit()
        
        # Add tracking update
        tracking = OrderTracking(
            order_id=order.id,
            status=status,
            location='AaplaBazaar Fulfillment Center',
            description=f'Order status updated to {status}'
        )
        db.session.add(tracking)
        db.session.commit()
        
        # Send SMS notification
        user = User.query.get(order.user_id)
        message = f"AaplaBazaar Update: Your order #{order.id} status has been updated to {status}. Track your order with ID: {order.tracking_number}"
        send_sms_notification(user.phone, message)
        
        flash(f'Order status updated to {status}!', 'success')
    
    return redirect(url_for('admin_order_detail', order_id=order.id))

# GI Tagged Products
@app.route('/gi-tagged-products')
def gi_tagged_products():
    gi_products = Product.query.filter_by(is_gi_tagged=True).all()
    return render_template('gi_tagged_products.html',
                           title='GI Tagged Products',
                           products=gi_products)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
