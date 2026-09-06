"""
Seed data for the seed_products management command. Image filenames
below reference files expected in seed_images/ just as they were
downloaded and name.  Categories and products
get added incrementally. """

CATEGORIES = [
    {"name": "Ankara Fabrics", "description": "Authentic wax print and lace fabric bundles, sold by the yard."},
    {"name": "Spices & Sauce Kits", "description": "Pre-measured spice blends for authentic West African cooking."},
    {"name": "Homeware", "description": "Kitchen, dining, and bedding pieces for the home."},
    {"name": "Beads & Jewellery", "description": "Handmade beaded and traditional jewellery for men and women."},
    {"name": "Accessories", "description": "Bags and footwear with West African design influence."},
    {"name": "Traditional Wear", "description": "Ready-to-wear traditional and cultural clothing."},
]

PRODUCTS = [
    {
        "name": "Jollof Rice Spice Kit",
        "category": "Spices & Sauce Kits",
        "description": "A pre-measured blend of smoked paprika, thyme, curry powder, and dried chili built specifically for party-style jollof rice. Just add tomatoes, pepper, and rice for the real thing without hunting down eight separate jars.",
        "price": 11.50,
        "stock_quantity": 30,
        "is_featured": True,
        "images": ["spices-sauces-kit-01-a.jpg", "spices-sauces-kit-01-b.jpg"],
    },
    {
        "name": "Suya Spice Blend (Yaji)",
        "category": "Spices & Sauce Kits",
        "description": "A ground peanut and pepper suya spice mix, the same blend used by roadside suya sellers across Nigeria. Rub it onto grilled beef, chicken, or even vegetables for a smoky, peppery crust.",
        "price": 9.99,
        "stock_quantity": 25,
        "is_featured": True,
        "images": ["spices-sauces-kit-02-a.jpg", "spices-sauces-kit-02-b.jpg"],
    },
    {
        "name": "Egusi Soup Spice Mix",
        "category": "Spices & Sauce Kits",
        "description": "The seasoning base for a proper pot of egusi soup, ground crayfish, stock cubes, and pepper blended together so the melon seeds are the only other thing you need to add.",
        "price": 12.25,
        "stock_quantity": 20,
        "images": ["spices-sauces-kit-03-a.jpg", "spices-sauces-kit-03-b.jpg", "spices-sauces-kit-03-c.jpg"],
    },
    {
        "name": "Pepper Soup Spice Kit",
        "category": "Spices & Sauce Kits",
        "description": "A warming blend of uziza, calabash nutmeg, and pepper soup spice for the classic Nigerian pepper soup, good with goat meat, chicken, or fish.",
        "price": 10.75,
        "stock_quantity": 20,
        "images": ["spices-sauces-kit-04-a.jpg", "spices-sauces-kit-04-b.jpg"],
    },
    {
        "name": "Ogbono Soup Starter Kit",
        "category": "Spices & Sauce Kits",
        "description": "Ground ogbono seeds paired with the stock and pepper blend needed to get the soup's signature draw right on the first try, a shortcut for one of the trickier soups to get consistent.",
        "price": 13.00,
        "stock_quantity": 18,
        "images": ["spices-sauces-kit-05-a.jpg", "spices-sauces-kit-05-b.jpg", "spices-sauces-kit-05-c.jpg"],
    },
    {
        "name": "Efo Riro Seasoning Blend",
        "category": "Spices & Sauce Kits",
        "description": "A seasoning blend built for efo riro, pepper, crayfish, and stock, so the vegetable soup base is ready before the spinach even hits the pot.",
        "price": 10.50,
        "stock_quantity": 20,
        "images": ["spices-sauces-kit-06-a.jpg", "spices-sauces-kit-06-b.jpg"],
    },
    {
        "name": "Banga Soup Spice Kit",
        "category": "Spices & Sauce Kits",
        "description": "The spice blend behind banga soup's distinct flavour, measured out and ready to combine with palm fruit concentrate.",
        "price": 13.50,
        "stock_quantity": 15,
        "images": ["spices-sauces-kit-07-a.jpg", "spices-sauces-kit-07-b.jpg"],
    },
    {
        "name": "Ata Rodo Pepper Blend",
        "category": "Spices & Sauce Kits",
        "description": "A dried and ground scotch bonnet pepper blend, the base heat behind most Nigerian stews and sauces, for anyone who wants real heat without roasting fresh peppers themselves.",
        "price": 8.99,
        "stock_quantity": 25,
        "images": ["spices-sauces-kit-08-a.jpg", "spices-sauces-kit-08-b.jpg"],
    },
    {
        "name": "Native Curry & Thyme Blend",
        "category": "Spices & Sauce Kits",
        "description": "A curry and thyme forward seasoning blend used across native soups and stews, a pantry staple rather than a single-dish specialty.",
        "price": 9.50,
        "stock_quantity": 22,
        "images": ["spices-sauces-kit-09-a.jpg", "spices-sauces-kit-09-b.jpg", "spices-sauces-kit-09-c.jpg"],
    },
]

REVIEWER_USERNAMES = [
    "amaka_t", "kwame_o", "ngozi_b", "tunde_f", "aisha_r", "chidi_m", "folake_s", "ebuka_n",
]

# Grouped by rating so a 5-star review never accidentally reads lukewarm.
REVIEW_POOL = {
    5: [
        ("Exactly as described", "This is exactly what I expected, great quality and arrived well packaged."),
        ("Really happy with this", "Bought this as a gift and ended up keeping it for myself instead."),
        ("Will buy again", "Second time ordering this one. Consistent quality every time."),
    ],
    4: [
        ("Good quality", "Solid product, does exactly what it says. Minor delay in delivery but worth the wait."),
        ("Would recommend", "Good value for the price. Colour is slightly different in person but still nice."),
    ],
    3: [
        ("It's okay", "Does the job but nothing special. Packaging could be better."),
        ("Decent for the price", "Fair quality for what I paid. Might try a different variant next time."),
    ],
}