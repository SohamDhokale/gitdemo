from app import app, db
from models import Product

# Function to get appropriate image URLs based on category and index
def get_image_urls(category, index=0):
    # Base URLs for Pinterest image links
    base_urls = {
        'clothing': [
            'https://media.istockphoto.com/id/93355119/photo/indian-saris.jpg?s=612x612&w=0&k=20&c=afmfiTJg0VAmIY6P_TJ_JYsTfGhUdevv18WXQRUZ8NQ=',  # Saree
            'https://i.pinimg.com/originals/c8/15/06/c815069a982ea98bd3f217d684376ce4.jpg',  # Kurta
            'https://weaverstory.com/cdn/shop/articles/Contemporary_Men_s_Pashmina_Shawls_by_Weaver_Story.png?v=1679565581',  # Pashmina
        ],
        'handicrafts': [
            'https://bidrihandicraft.com/image/catalog/144.png',  # Vase
            'https://m.media-amazon.com/images/I/81IAQvh50AL._SL1500_.jpg',  # Brass figurine
            'https://3.imimg.com/data3/QK/TP/MY-9091856/blue-pottery-250x250.jpg'   # Blue pottery
        ],
        'spices': [
            'https://www.kiril-mischeff.com/wp-content/uploads/2021/01/kiril-mischeff-product-chilli.jpg',  # Chilli
            'https://images.healthshots.com/healthshots/en/uploads/2022/05/27213440/benefits-of-saffron-1600x900.jpg',  # Saffron
            'https://domf5oio6qrcr.cloudfront.net/medialibrary/15065/conversions/fa246ce0-054b-4892-bf30-5eb43cd938aa-thumb.jpg'   # Turmeric
        ],
        'jewelry': [
            'https://retailjewellerindia.com/wp-content/uploads/2020/01/Quota-creative-23-01-2020-Kundan-1.jpg',  # Kundan set
            'https://www.krishnajewellers.com/blog/wp-content/uploads/2021/11/gold-vaddanam-design.jpg',  # Temple jewelry
            'https://media.istockphoto.com/id/1277517088/photo/fancy-designer-antique-golden-bracelets-for-woman-fashion.jpg?s=612x612&w=0&k=20&c=n49O0S5rIgzxJX5bU1YjwRHfou0DYPcmsv-N5JAAM14='   # Bangles
        ],
        'home_decor': [
            'https://thumbs.dreamstime.com/b/madhubani-painting-8294267.jpg',  # Madhubani
            'https://www.dwoodchettinadpillars.com/images/image-5.jpg',  # Wooden pillars
            'https://www.villagesquare.in/wp-content/uploads/2022/09/Lead-alt-02.jpg'   # Carpet
        ],
        'food_products': [
            'https://images.unsplash.com/photo-1664791461482-79f5deee490f?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bWFuZ28lMjBwaWNrbGV8ZW58MHx8MHx8fDA%3D',  # Pickle
            'https://www.goldentipstea.in/cdn/shop/articles/Perfect-brew-blog-banner_1_1024x.png?v=1617879752',  # Tea
            'https://www.ruraltreasures.com/cdn/shop/articles/NbmkT7xqOx5VE9X8ZzK5TXIEvvJ0bpwnhJfEi2gd.jpg?v=1644053684'   # Jaggery
        ],
        'beauty': [
            'hhttps://m.media-amazon.com/images/I/71DublkdqFL.jpg',  # Sandalwood soap
            'https://skinrange.com/cdn/shop/files/hair_care-1.jpg?v=1685361306&width=3840',  # Hair oil
            'https://5.imimg.com/data5/SELLER/Default/2020/9/YB/NL/ZT/71343896/ayurvedic-mask-500x500.jpeg'   # Face mask
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

# List of products by category
product_data = [
    # Clothing Category
    {
        'name': 'Handwoven Cotton Saree',
        'description': 'Traditional handwoven cotton saree with intricate border designs. Made by skilled artisans in Bengal using ancient weaving techniques. Perfect for both casual wear and special occasions.',
        'price': 2499.00,
        'discount_price': 1999.00,
        'stock': 50,
        'category': 'clothing',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Handloom sarees from West Bengal with GI tag protection since 2007, known for their distinctive traditional designs and weaving techniques.',
        'origin': 'West Bengal'
    },
    {
        'name': 'Men\'s Khadi Kurta',
        'description': 'Elegant khadi cotton kurta for men, handspun and handwoven in Gujarat. Features traditional embroidery with a contemporary fit. Comfortable and sustainable clothing option.',
        'price': 1299.00,
        'discount_price': 999.00,
        'stock': 75,
        'category': 'clothing',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Gujarat'
    },
    {
        'name': 'Pashmina Shawl',
        'description': 'Luxurious hand-woven pashmina shawl from Kashmir. Made from the fine wool obtained from Changthangi goats. Each piece features intricate traditional patterns that take weeks to complete.',
        'price': 5999.00,
        'discount_price': 5499.00,
        'stock': 25,
        'category': 'clothing',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Kashmir Pashmina received GI certification in 2008, protecting this centuries-old craft of creating shawls from fine Changthangi goat wool.',
        'origin': 'Jammu & Kashmir'
    },
    
    # Handicrafts Category
    {
        'name': 'Bidri Art Vase',
        'description': 'Traditional Bidri art vase handcrafted in Bidar, Karnataka. Features intricate silver inlay work on a blackened alloy of zinc and copper. Each piece is unique and takes weeks to complete.',
        'price': 4500.00,
        'discount_price': None,
        'stock': 15,
        'category': 'handicrafts',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Bidri ware received GI tag protection in 2005, recognizing this 14th-century craft of creating metalware with silver inlay unique to Bidar, Karnataka.',
        'origin': 'Karnataka'
    },
    {
        'name': 'Dhokra Brass Figurine',
        'description': 'Traditional Dhokra brass figurine made using the lost-wax casting technique. Handcrafted by tribal artisans of Bastar, these figurines depict rural life, folklore and tribal deities.',
        'price': 1899.00,
        'discount_price': 1699.00,
        'stock': 30,
        'category': 'handicrafts',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Dhokra brass craft is a 4,000-year-old metal casting technique practiced by the Dhokra Damar tribes, granted GI tag protection in 2018.',
        'origin': 'Chhattisgarh'
    },
    {
        'name': 'Blue Pottery Tea Set',
        'description': 'Beautiful hand-painted blue pottery tea set from Jaipur. Includes teapot and 6 cups with traditional floral designs. Made using calcium oxide, quartz, and multani mitti, fired at low temperatures.',
        'price': 2299.00,
        'discount_price': 1999.00,
        'stock': 20,
        'category': 'handicrafts',
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Rajasthan'
    },
    
    # Spices Category
    {
        'name': 'Guntur Red Chilli Powder',
        'description': 'Authentic Guntur red chilli powder known for its distinctive color and medium-hot pungency. Sourced directly from farmers in Guntur, Andhra Pradesh. Perfect for traditional South Indian dishes.',
        'price': 299.00,
        'discount_price': 249.00,
        'stock': 100,
        'category': 'spices',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Guntur Sannam Chilli received GI tag protection in 2019, recognizing its unique flavor profile and cultivation techniques specific to this region.',
        'origin': 'Andhra Pradesh'
    },
    {
        'name': 'Kashmir Saffron',
        'description': 'Premium quality Kashmir saffron, known as the world\'s finest saffron with distinct aroma, flavor, and color. Harvested by hand from the Crocus sativus flower. Packaged in a 2g glass vial.',
        'price': 999.00,
        'discount_price': None,
        'stock': 30,
        'category': 'spices',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Kashmir Saffron received GI tag protection in 2020, recognizing its unique characteristics that come from the specific geography of Kashmir Valley.',
        'origin': 'Jammu & Kashmir'
    },
    {
        'name': 'Organic Turmeric Powder',
        'description': 'Organically grown turmeric powder from Erode, Tamil Nadu, known for its high curcumin content. Sustainably farmed, sun-dried, and ground. Ideal for cooking and medicinal purposes.',
        'price': 199.00,
        'discount_price': 179.00,
        'stock': 150,
        'category': 'spices',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Erode Turmeric received GI tag protection in 2019, known for its distinctive bright yellow color and high curcumin content.',
        'origin': 'Tamil Nadu'
    },
    
    # Jewelry Category
    {
        'name': 'Kundan Necklace Set',
        'description': 'Exquisite Kundan necklace set featuring traditional Rajasthani craftsmanship. Includes matching earrings. Handcrafted with gold foil, glass stones, and meenakari enamel work at the back.',
        'price': 12999.00,
        'discount_price': 10999.00,
        'stock': 10,
        'category': 'jewelry',
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Rajasthan'
    },
    {
        'name': 'Temple Jewelry Earrings',
        'description': 'Traditional South Indian temple jewelry earrings made with gold-plated brass and synthetic ruby stones. Features classic temple motifs and goddess designs inspired by ancient temple sculptures.',
        'price': 2499.00,
        'discount_price': 1999.00,
        'stock': 25,
        'category': 'jewelry',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Tamil Nadu'
    },
    {
        'name': 'Paachi Work Bangle Set',
        'description': 'Set of 6 traditional Paachi work bangles from Gujarat. Handcrafted with brass and adorned with colorful glass beads and mirrors. The intricate design represents traditional motifs passed down through generations.',
        'price': 1499.00,
        'discount_price': 1299.00,
        'stock': 30,
        'category': 'jewelry',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Gujarat'
    },
    
    # Home Decor Category
    {
        'name': 'Madhubani Painting',
        'description': 'Authentic Madhubani painting on handmade paper depicting rural life and mythology. Created by artists from Bihar using traditional techniques and natural pigments. Size: 15" x 20", unframed.',
        'price': 3499.00,
        'discount_price': 2999.00,
        'stock': 15,
        'category': 'home_decor',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Madhubani paintings received GI tag protection in 2007, recognizing this ancient folk art tradition from the Mithila region of Bihar.',
        'origin': 'Bihar'
    },
    {
        'name': 'Chettinad Pillars',
        'description': 'Antique reclaimed wooden pillars from Chettinad mansions. Handcarved with intricate details, these pillars are 100+ years old and make for stunning statement pieces in any home. Size: 6 feet tall.',
        'price': 24999.00,
        'discount_price': None,
        'stock': 5,
        'category': 'home_decor',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Tamil Nadu'
    },
    {
        'name': 'Kashmiri Hand-knotted Carpet',
        'description': 'Luxurious hand-knotted carpet from Kashmir featuring traditional Persian-inspired designs. Made with pure silk on a cotton base with 900+ knots per square inch. Size: 3\' x 5\'.',
        'price': 19999.00,
        'discount_price': 17999.00,
        'stock': 8,
        'category': 'home_decor',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Kashmiri Carpets received GI tag protection in 2016, recognizing this centuries-old craft of hand-knotting intricate carpets using specific techniques unique to Kashmir.',
        'origin': 'Jammu & Kashmir'
    },
    
    # Food Products Category
    {
        'name': 'Alphonso Mango Pickle',
        'description': 'Traditional homestyle Alphonso mango pickle made with premium Ratnagiri Alphonso mangoes. Prepared with mustard oil and a special blend of spices. No preservatives added. 250g glass jar.',
        'price': 349.00,
        'discount_price': 299.00,
        'stock': 50,
        'category': 'food_products',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Alphonso Mango from Ratnagiri, Maharashtra received GI tag protection in 2018, recognized for its unique taste, sweetness, and texture.',
        'origin': 'Maharashtra'
    },
    {
        'name': 'Darjeeling Tea Collection',
        'description': 'Premium Darjeeling tea collection featuring First Flush, Second Flush, and Autumn Flush teas. Sourced directly from heritage tea gardens in the Darjeeling hills. Set of 3 metal caddies, 50g each.',
        'price': 1299.00,
        'discount_price': 1099.00,
        'stock': 30,
        'category': 'food_products',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Darjeeling Tea was the first Indian product to receive GI tag protection in 2004, known worldwide as the "Champagne of Teas".',
        'origin': 'West Bengal'
    },
    {
        'name': 'Goan Coconut Jaggery',
        'description': 'Traditional Goan jaggery made from coconut palm sap. Naturally processed without chemicals, retaining all minerals and distinctive smoky caramel flavor. Perfect for traditional Goan sweets. 500g pack.',
        'price': 249.00,
        'discount_price': 199.00,
        'stock': 75,
        'category': 'food_products',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Goa'
    },
    
    # Beauty Category
    {
        'name': 'Mysore Sandalwood Soap',
        'description': 'Authentic Mysore sandalwood soap made with pure sandalwood oil and traditional methods. Known for its distinctive fragrance and skin benefits. Handcrafted in small batches. 75g bar.',
        'price': 249.00,
        'discount_price': 199.00,
        'stock': 100,
        'category': 'beauty',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Mysore Sandalwood Oil received GI tag protection in 2005, known for its distinctive fragrance and therapeutic properties.',
        'origin': 'Karnataka'
    },
    {
        'name': 'Ayurvedic Hair Oil Blend',
        'description': 'Traditional Ayurvedic hair oil made with a blend of herbs including Brahmi, Amla, and Bhringraj in a sesame oil base. Prepared according to ancient Ayurvedic texts. 200ml glass bottle.',
        'price': 449.00,
        'discount_price': 399.00,
        'stock': 60,
        'category': 'beauty',
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Kerala'
    },
    {
        'name': 'Rose-Saffron Face Mask',
        'description': 'Luxury face mask powder made with Himalayan rose petals and premium Kashmir saffron. Handcrafted in small batches using traditional methods. Mix with raw honey or yogurt before application. 50g jar.',
        'price': 699.00,
        'discount_price': 599.00,
        'stock': 40,
        'category': 'beauty',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Uttarakhand'
    },
    
    # Accessories Category
    {
        'name': 'Banarasi Silk Clutch',
        'description': 'Elegant clutch purse made with genuine Banarasi silk brocade. Features traditional gold zari work and detachable chain strap. Handcrafted by artisans in Varanasi. Size: 8" x 4".',
        'price': 1899.00,
        'discount_price': 1599.00,
        'stock': 25,
        'category': 'accessories',
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Banarasi Brocade received GI tag protection in 2009, protecting this 500-year-old weaving tradition from Varanasi.',
        'origin': 'Uttar Pradesh'
    },
    {
        'name': 'Kolhapuri Leather Chappal',
        'description': 'Authentic handcrafted Kolhapuri leather chappals (sandals) from Maharashtra. Made with vegetable-tanned leather using traditional techniques. Known for durability and distinctive style.',
        'price': 999.00,
        'discount_price': 849.00,
        'stock': 40,
        'category': 'accessories',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Kolhapuri Chappal received GI tag protection in 2019, recognizing the unique leather crafting techniques specific to the Kolhapur region.',
        'origin': 'Maharashtra'
    },
    {
        'name': 'Chanderi Silk Stole',
        'description': 'Lightweight Chanderi silk stole with traditional zari border and small bootis. Handwoven in Chanderi, Madhya Pradesh, this stole blends silk and cotton for a beautiful drape. Size: 2m x 0.5m.',
        'price': 899.00,
        'discount_price': 799.00,
        'stock': 60,
        'category': 'accessories',
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Chanderi Fabric received GI tag protection in 2005, protecting this traditional weaving technique that dates back to the Vedic period.',
        'origin': 'Madhya Pradesh'
    },
    
    # Books Category
    {
        'name': 'Illustrated History of Indian Art',
        'description': 'Comprehensive hardcover book documenting the evolution of Indian art from ancient cave paintings to contemporary works. Features 300+ color illustrations and expert commentary. 350 pages.',
        'price': 2499.00,
        'discount_price': 2199.00,
        'stock': 20,
        'category': 'books',
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Delhi'
    },
    {
        'name': 'Traditional Indian Recipes',
        'description': 'Collection of authentic regional recipes from across India, passed down through generations. Includes detailed cooking techniques, ingredient substitutions, and cultural context. 250 recipes, 400 pages.',
        'price': 1299.00,
        'discount_price': 1099.00,
        'stock': 35,
        'category': 'books',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Mumbai'
    },
    {
        'name': 'Crafts of India: A Photographic Journey',
        'description': 'Award-winning coffee table book showcasing India\'s diverse craft traditions through stunning photography. Features artisan stories, historical context, and regional techniques. 200 pages, hardcover.',
        'price': 2999.00,
        'discount_price': 2699.00,
        'stock': 15,
        'category': 'books',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Bengaluru'
    },
    
    # Electronics Category
    {
        'name': 'Smart Yoga Mat',
        'description': 'Innovative yoga mat with embedded sensors to track posture, balance, and movement. Connects to mobile app for real-time feedback and guided sessions. Made with eco-friendly materials. Size: 72" x 24".',
        'price': 5999.00,
        'discount_price': 4999.00,
        'stock': 20,
        'category': 'electronics',
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Bengaluru'
    },
    {
        'name': 'Digital Tanpura',
        'description': 'Electronic tanpura with authentic sound reproduction for classical Indian music practice. Features 4 strings, multiple tuning options, and 24-hour battery life. Compact and portable design.',
        'price': 3499.00,
        'discount_price': 3199.00,
        'stock': 15,
        'category': 'electronics',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Pune'
    },
    {
        'name': 'Solar Spice Grinder',
        'description': 'Eco-friendly solar-powered spice grinder perfect for Indian kitchens. Features ceramic grinding mechanism, adjustable coarseness, and backup battery. Ideal for fresh masalas and spice blends.',
        'price': 1299.00,
        'discount_price': 1099.00,
        'stock': 25,
        'category': 'electronics',
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Chennai'
    }
]

# Adding image URLs to products using our function
products = []
for i, product in enumerate(product_data):
    category = product['category']
    main_img, second_img = get_image_urls(category, i % 3)  # Use i%3 to cycle through the 3 images for each category
    
    # Create copy of the product data with images
    product_with_images = product.copy()
    product_with_images['image_url1'] = main_img
    product_with_images['image_url2'] = second_img
    product_with_images['image_url3'] = None
    
    products.append(product_with_images)

# Create the products in the database
with app.app_context():
    # First, clear all existing products
    Product.query.delete()
    db.session.commit()
    
    # Then add the new products with Pinterest images
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print(f"Added {len(products)} products to the database with Pinterest images.")