# tracker.py

import time
import json
from scraper import aggregate_results

# You can customize this interval in seconds
CHECK_INTERVAL = 3600  # 1 hour

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

def send_notification(results):
    # Stubbed for now – will link with Twilio/WhatsApp later
    for r in results:
        print(f"🔥 Deal Found: {r['title']} at ₹{r['price']} [{r['site']}] → {r['link']}")

def track_deals():
    config = load_config()
    all_results = []
    for product in config["products"]:
        name = product["name"]
        min_price = product["min_price"]
        max_price = product["max_price"]
        sites = product.get("sites", ["Amazon", "Flipkart", "Myntra"])

        print(f"\n🔍 Checking for '{name}' on {', '.join(sites)}...")
        results = aggregate_results(name, min_price, max_price, sites)
        if results:
            send_notification(results)
        all_results.extend(results)
    save_results(all_results)

if __name__ == "__main__":
    while True:
        track_deals()
        print(f"\n⏳ Waiting {CHECK_INTERVAL} seconds until next check...\n")
        time.sleep(CHECK_INTERVAL)
