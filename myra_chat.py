def greet_user():
    print("👋 Hey there! I'm Myra, your AI shopping bestie.")
    print("Tell me what you’re looking for, and I’ll hunt it down for you like a deal detective 🕵️‍♀️")

def get_user_preferences():
    # Not used directly since Streamlit takes input, but we keep it for CLI fallback or future bots.
    print("Let’s set up your wishlist:")

    product = input("🔍 What product are you looking for? ")
    min_price = int(input("💸 Minimum price (₹): "))
    max_price = int(input("💰 Maximum price (₹): "))
    sites = input("🛒 Preferred sites (comma-separated: Amazon, Flipkart): ").split(',')
    category = input("📦 Category (Electronics, Home, Fashion): ")
    phone_number = input("📱 Your WhatsApp number (+91 format): ")

    return {
        "product": product.strip(),
        "min_price": min_price,
        "max_price": max_price,
        "sites": [site.strip() for site in sites],
        "category": category.strip(),
        "phone": phone_number.strip()
    }
