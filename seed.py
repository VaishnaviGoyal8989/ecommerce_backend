from app.core.database import SessionLocal
from app.products.models import Product

# Create DB session
db = SessionLocal()

# Sample product data
sample_products = [
    {
        "name": "Wireless Mouse",
        "description": " wireless mouse for your device",
        "price": 599.00,
        "stock": 100,
        "category": "Electronics",
        "image_url": "https://example.com/images/mouse.jpg"
    },
    {
        "name": "Bluetooth Speaker",
        "description": "Portable speaker with HD sound and bass",
        "price": 1299.00,
        "stock": 50,
        "category": "Electronics",
        "image_url": "https://example.com/images/speaker.jpg"
    },
    {
        "name": "Running Shoes",
        "description": "Comfortable sports shoes for daily use",
        "price": 2199.00,
        "stock": 70,
        "category": "Footwear",
        "image_url": "https://example.com/images/shoes.jpg"
    },
]

# Insert into DB
for prod in sample_products:
    product = Product(**prod)
    db.add(product)

db.commit()
db.close()

print("Sample products seeded.")