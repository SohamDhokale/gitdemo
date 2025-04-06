from app import app, db
from models import Product

# Clear existing products if needed
# Product.query.delete()
# db.session.commit()

# Function to get appropriate image URLs based on category and index
def get_image_urls(category, index=0):
    # Base URLs for reliable placeholder images
    base_urls = {
        'clothing': [
            'https://plus.unsplash.com/premium_photo-1682096862492-a341635a56ce?q=80&w=800',
            'https://images.unsplash.com/photo-1589248723605-75830671837c?q=80&w=800',
            'https://images.unsplash.com/photo-1639269685067-2585aefdcf60?q=80&w=800',
        ],
        'handicrafts': [
            'https://images.unsplash.com/photo-1597696929736-6d13bed8e6a8?q=80&w=800',
            'https://images.unsplash.com/photo-1566885594836-26889f7a34c4?q=80&w=800', 
            'https://images.unsplash.com/photo-1530105025495-181e33ad4363?q=80&w=800'
        ],
        'spices': [
            'https://images.unsplash.com/photo-1532336414049-cf22c39e258f?q=80&w=800',
            'https://images.unsplash.com/photo-1599720843413-fe551e54641a?q=80&w=800',
            'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?q=80&w=800'
        ],
        'jewelry': [
            'https://images.unsplash.com/photo-1601121141461-9d6647bca1ed?q=80&w=800',
            'https://images.unsplash.com/photo-1573408301185-9146fe634ad0?q=80&w=800',
            'https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=800'
        ],
        'home_decor': [
            'https://images.unsplash.com/photo-1513519245088-0e12902e5a38?q=80&w=800',
            'https://images.unsplash.com/photo-1578500351865-d6c3276abfb7?q=80&w=800',
            'https://images.unsplash.com/photo-1594115808390-6e2a36278144?q=80&w=800'
        ],
        'food_products': [
            'https://images.unsplash.com/photo-1584057388243-26451a933771?q=80&w=800',
            'https://images.unsplash.com/photo-1532634922-8fe0b757fb13?q=80&w=800',
            'https://images.unsplash.com/photo-1585059895524-72359e06133a?q=80&w=800'
        ],
        'beauty': [
            'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?q=80&w=800',
            'https://images.unsplash.com/photo-1619451683205-e7a68fed5628?q=80&w=800',
            'https://images.unsplash.com/photo-1591375372156-542495912da9?q=80&w=800'
        ],
        'accessories': [
            'https://images.unsplash.com/photo-1584917865442-de89df76afd3?q=80&w=800',
            'https://images.unsplash.com/photo-1588444650733-d9726c53d1b2?q=80&w=800',
            'https://images.unsplash.com/photo-1509941943102-10c232535736?q=80&w=800'
        ],
        'books': [
            'https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=800',
            'https://images.unsplash.com/photo-1519682337058-a94d519337bc?q=80&w=800',
            'https://images.unsplash.com/photo-1467951591042-f388365db261?q=80&w=800'
        ],
        'electronics': [
            'https://images.unsplash.com/photo-1550009158-9ebf69173e03?q=80&w=800',
            'https://images.unsplash.com/photo-1468495244123-6c6c332eeece?q=80&w=800',
            'https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=800'
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
    for product_data in products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    print(f"Added {len(products)} products to the database.")