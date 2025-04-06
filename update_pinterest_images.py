from app import app, db
from models import Product

# Function to get appropriate image URLs based on category and index
def get_image_urls(category, index=0):
    # Base URLs for Pinterest image links
    base_urls = {
        'clothing': [
            'https://i.pinimg.com/564x/85/6c/62/856c62a709e0c78c9d30f56c96d5f142.jpg',  # Saree
            'https://i.pinimg.com/564x/98/25/0d/98250d035550b57b2d9dd800f0ff3c84.jpg',  # Kurta
            'https://i.pinimg.com/564x/78/83/cb/7883cb3ea33b71b8a8f8d73255282b0a.jpg',  # Pashmina
        ],
        'handicrafts': [
            'https://i.pinimg.com/564x/d8/7c/ca/d87cca88c576a7c868754ef9853ed307.jpg',  # Vase
            'https://i.pinimg.com/564x/5b/75/4d/5b754d72f20b8d53b5c2dd71a43bf2d9.jpg',  # Brass figurine
            'https://i.pinimg.com/564x/e3/25/99/e32599e6a06c1a1f04a7a184f89df2c9.jpg'   # Blue pottery
        ],
        'spices': [
            'https://i.pinimg.com/564x/dd/ee/9a/ddee9a5f1a1e987e4c3d9c86008eedcd.jpg',  # Chilli
            'https://i.pinimg.com/564x/78/22/ee/7822eeafde78a2c0f70aec6b31ea0ed6.jpg',  # Saffron
            'https://i.pinimg.com/564x/6a/ff/ce/6affce0ccda6eef3717de52dcf7399eb.jpg'   # Turmeric
        ],
        'jewelry': [
            'https://i.pinimg.com/564x/94/89/41/948941d8e40c64c0bbaa9f8da9526731.jpg',  # Kundan set
            'https://i.pinimg.com/564x/6a/06/97/6a06971be92a47ccc8de9fb9d5e97f64.jpg',  # Temple jewelry
            'https://i.pinimg.com/564x/de/c8/5c/dec85c8b5f2d36ad75a470747c824c9f.jpg'   # Bangles
        ],
        'home_decor': [
            'https://i.pinimg.com/564x/7c/70/3e/7c703e4d994fc5451c2ddf37e23c8034.jpg',  # Madhubani
            'https://i.pinimg.com/564x/a7/eb/8e/a7eb8e61ebce3ad80b9507d13d72cbab.jpg',  # Wooden pillars
            'https://i.pinimg.com/564x/a3/de/c1/a3dec12a0fc0eb3c1b7223dea9da9ed7.jpg'   # Carpet
        ],
        'food_products': [
            'https://i.pinimg.com/564x/97/fd/8e/97fd8e8e83b7ea1dc0b4d422bfa0a106.jpg',  # Pickle
            'https://i.pinimg.com/564x/71/23/ab/7123ab85318c8c063e28c4f4d8c3fcb7.jpg',  # Tea
            'https://i.pinimg.com/564x/18/9b/c9/189bc9ebed1c79e4fce72f85f0b4bf30.jpg'   # Jaggery
        ],
        'beauty': [
            'https://i.pinimg.com/564x/4c/09/78/4c09784f73ed3a8fb88c0e472c4db636.jpg',  # Sandalwood soap
            'https://i.pinimg.com/564x/92/18/27/92182717d69a1c9c31c4a671dc6e6100.jpg',  # Hair oil
            'https://i.pinimg.com/564x/a3/14/07/a3140733e88d33c1b059e1976f9a654c.jpg'   # Face mask
        ],
        'accessories': [
            'https://i.pinimg.com/564x/07/c4/e7/07c4e7ae0ec04e9ae47a88d933e3bb27.jpg',  # Clutch
            'https://i.pinimg.com/564x/79/da/a5/79daa5e5a987be8c53e30efd6bb045cd.jpg',  # Kolhapuri
            'https://i.pinimg.com/564x/61/22/7c/61227c6ea5b9cf04d0e0f9c35cb2b7a5.jpg'   # Stole
        ],
        'books': [
            'https://i.pinimg.com/564x/0a/86/41/0a86412f1a6b8d5dde8c4be29a10c88a.jpg',  # Art book
            'https://i.pinimg.com/564x/c1/0c/d4/c10cd44e86351948c92091c0b9a92e65.jpg',  # Recipe book
            'https://i.pinimg.com/564x/d9/2d/ee/d92dee61b7a7c4de0b263176d9865fb3.jpg'   # Craft book
        ],
        'electronics': [
            'https://i.pinimg.com/564x/69/3b/50/693b5055fc5e14b9d7d5f17523b72b0a.jpg',  # Yoga mat
            'https://i.pinimg.com/564x/de/e5/e1/dee5e154fb5bee20d8d6ce5198577a47.jpg',  # Tanpura
            'https://i.pinimg.com/564x/d4/d0/f3/d4d0f3372578b19d33064ed42c4aba3a.jpg'   # Grinder
        ]
    }
    
    # Default category in case the provided one is not found
    default_category = 'clothing'
    
    # Get images for the specified category or default to clothing
    images = base_urls.get(category, base_urls[default_category])
    
    # Return the image at the given index or the first one if index is out of bounds
    main_image = images[index % len(images)]
    second_image = images[(index + 1) % len(images)] if len(images) > 1 else None
    
    return main_image, second_image

# Update existing products with new images
with app.app_context():
    # Get all products grouped by category
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    update_count = 0
    
    # Process each category
    for category in categories:
        # Get products in this category
        products = Product.query.filter_by(category=category).all()
        
        # Update each product with appropriate Pinterest images
        for i, product in enumerate(products):
            main_img, second_img = get_image_urls(category, i)
            product.image_url1 = main_img
            product.image_url2 = second_img
            product.image_url3 = None
            update_count += 1
    
    # Commit all changes
    db.session.commit()
    print(f"Updated images for {update_count} products with Pinterest images.")