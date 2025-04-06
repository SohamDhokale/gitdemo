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
products = [
    # Clothing Category
    {
        'name': 'Handwoven Cotton Saree',
        'description': 'Traditional handwoven cotton saree with intricate border designs. Made by skilled artisans in Bengal using ancient weaving techniques. Perfect for both casual wear and special occasions.',
        'price': 2499.00,
        'discount_price': 1999.00,
        'stock': 50,
        'category': 'clothing',
        'image_url1': 'https://images.unsplash.com/photo-1610189844977-2ed7a7a3b1e7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'image_url2': 'https://images.unsplash.com/photo-1610189844990-08714fe90dbd?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80',
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1598374211636-dcc979469a52',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1575574835265-ba28c21c9c11',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1605883705077-8d3d75941642',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1607344645866-8d0c5d232faa',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1594736797933-d0501ba2fe65',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1579910801235-70d99a84d2d7',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1599543255683-1fb265b4bf6e',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1615484527693-352542b57489',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1611652022419-a9419f74628c',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1630019852942-7a3592568ed0',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1611591437268-6cthb1b0270d',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1582210715397-aefea00b47ad',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1609235711761-77a852a45832',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1584286595840-e2a279ce9d28',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1589217157232-464b505b197a',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1564890369478-c89ca6d9cde9',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1586698990195-7d14235fcdf5',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1612886951223-d94a06c704ef',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1608248597279-f99d160beba3',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1608613304903-80f2b2df685b',
        'image_url2': None,
        'image_url3': None,
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
        'image_url1': 'https://images.unsplash.com/photo-1591910849983-3b57a8f9954d',
        'image_url2': None,
        'image_url3': None,
        'is_featured': True,
        'is_gi_tagged': True,
        'gi_tag_details': 'Banarasi brocades and sarees received GI tag protection in 2009, known for their gold and silver zari work and intricate designs.',
        'origin': 'Uttar Pradesh'
    },
    {
        'name': 'Kolhapuri Leather Sandals',
        'description': 'Authentic Kolhapuri chappal handcrafted by traditional artisans from Kolhapur. Made with vegetable-tanned leather using techniques passed down through generations. Available in multiple sizes.',
        'price': 1299.00,
        'discount_price': 999.00,
        'stock': 40,
        'category': 'accessories',
        'image_url1': 'https://images.unsplash.com/photo-1591910180595-5ac96efab27c',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Kolhapuri Chappal received GI tag protection in 2019, recognizing this 800-year-old handcrafting tradition native to Kolhapur, Maharashtra.',
        'origin': 'Maharashtra'
    },
    {
        'name': 'Ikat Cotton Tote Bag',
        'description': 'Handwoven cotton tote bag featuring traditional Pochampally Ikat patterns. Each piece is hand-dyed and woven by skilled artisans in Telangana. Fair trade and sustainable. Size: 14" x 16".',
        'price': 799.00,
        'discount_price': 699.00,
        'stock': 70,
        'category': 'accessories',
        'image_url1': 'https://images.unsplash.com/photo-1589221962236-7aab841d5f4e',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': True,
        'gi_tag_details': 'Pochampally Ikat received GI tag protection in 2005, known for its geometric patterns created through the distinctive resist-dyeing technique.',
        'origin': 'Telangana'
    },
    
    # Books Category
    {
        'name': 'The Art of Indian Textiles',
        'description': 'Comprehensive hardcover book exploring the rich tradition of Indian textiles across different regions. Features 200+ color photographs, detailed historical context, and artisan interviews. 256 pages.',
        'price': 1999.00,
        'discount_price': 1799.00,
        'stock': 20,
        'category': 'books',
        'image_url1': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Delhi'
    },
    {
        'name': 'Traditional Indian Cooking',
        'description': 'Award-winning cookbook featuring 150+ authentic recipes from various Indian regions, along with cultural context and cooking techniques. Includes vegetarian, non-vegetarian, and vegan options.',
        'price': 1499.00,
        'discount_price': 1299.00,
        'stock': 35,
        'category': 'books',
        'image_url1': 'https://images.unsplash.com/photo-1589998059171-988d887df646',
        'image_url2': None,
        'image_url3': None,
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Mumbai'
    },
    {
        'name': 'Illustrated History of Indian Art',
        'description': 'Scholarly yet accessible guide to 5000 years of Indian art history, from ancient cave paintings to contemporary works. Features timelines, artist profiles, and cultural context. 320 pages with full-color illustrations.',
        'price': 2499.00,
        'discount_price': 2199.00,
        'stock': 15,
        'category': 'books',
        'image_url1': 'https://images.unsplash.com/photo-1532068306628-96963a635ba9',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Chennai'
    },
    
    # Electronics Category
    {
        'name': 'Digital Tanpura',
        'description': 'Electronic tanpura featuring authentic sound samples recorded from a professional acoustic tanpura. Offers 4 strings, adjustable pitch and volume, and rechargeable battery that lasts 12+ hours.',
        'price': 4999.00,
        'discount_price': 4499.00,
        'stock': 15,
        'category': 'electronics',
        'image_url1': 'https://images.unsplash.com/photo-1589491106922-a8e488c4206f',
        'image_url2': None,
        'image_url3': None,
        'is_featured': True,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Pune'
    },
    {
        'name': 'Smart Pressure Cooker',
        'description': 'Modern smart pressure cooker designed specifically for Indian cooking. Features 12 preset programs for dishes like biryani, dal, and curry. App-connected with timer and pressure monitoring.',
        'price': 5999.00,
        'discount_price': 4999.00,
        'stock': 25,
        'category': 'electronics',
        'image_url1': 'https://images.unsplash.com/photo-1585664156547-779321ff40be',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Bangalore'
    },
    {
        'name': 'Bamboo Phone Amplifier',
        'description': 'Eco-friendly phone amplifier handcrafted from sustainable bamboo. Naturally amplifies sound without electricity. Designed and crafted by tribal artisans from the Northeast using traditional techniques.',
        'price': 899.00,
        'discount_price': 799.00,
        'stock': 40,
        'category': 'electronics',
        'image_url1': 'https://images.unsplash.com/photo-1588957802836-e64c34761959',
        'image_url2': None,
        'image_url3': None,
        'is_featured': False,
        'is_gi_tagged': False,
        'gi_tag_details': None,
        'origin': 'Assam'
    }
]

# Add all products
with app.app_context():
    # Check if products table is empty
    if Product.query.count() == 0:
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        db.session.commit()
        print(f"Added {len(products)} products to the database.")
    else:
        print("Products already exist in the database.")