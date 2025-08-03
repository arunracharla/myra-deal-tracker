# scraper.py

import requests
from bs4 import BeautifulSoup
import re
import json
import random
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def clean_price(text):
    price = re.findall(r"\d+[,\d]*", text)
    if price:
        return int(price[0].replace(",", ""))
    return None

def scrape_amazon(product_name, min_price, max_price):
    print("Scraping Amazon...")
    url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for div in soup.select(".s-result-item"):
        title = div.select_one("h2 span")
        price = div.select_one(".a-price-whole")
        link = div.select_one("h2 a")
        if title and price and link:
            actual_price = clean_price(price.text)
            if actual_price and min_price <= actual_price <= max_price:
                results.append({
                    "site": "Amazon",
                    "title": title.text.strip(),
                    "price": actual_price,
                    "link": "https://www.amazon.in" + link['href']
                })
    return results

def scrape_flipkart(product_name, min_price, max_price):
    print("Scraping Flipkart...")
    url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for div in soup.select("._1AtVbE"):
        title = div.select_one("._4rR01T") or div.select_one(".s1Q9rs")
        price = div.select_one("._30jeq3")
        link = div.select_one("a")
        if title and price and link:
            actual_price = clean_price(price.text)
            if actual_price and min_price <= actual_price <= max_price:
                results.append({
                    "site": "Flipkart",
                    "title": title.text.strip(),
                    "price": actual_price,
                    "link": "https://www.flipkart.com" + link['href']
                })
    return results

def scrape_myntra(product_name, min_price, max_price):
    print("Scraping Myntra...")
    # Myntra needs JS parsing or internal APIs; here we simulate the API call
    url = f"https://www.myntra.com/gateway/v2/search/{product_name.replace(' ', '%20')}"
    params = {"rawQuery": product_name, "rows": 20, "start": 0}

    try:
        res = requests.get(url, headers=HEADERS, params=params)
        data = res.json()
        items = data.get("data", {}).get("products", [])

        results = []
        for item in items:
            price = item.get("price", {}).get("discounted")
            if price and min_price <= price <= max_price:
                results.append({
                    "site": "Myntra",
                    "title": item.get("productName"),
                    "price": price,
                    "link": f"https://www.myntra.com/{item.get('landingPageUrl')}"
                })
        return results
    except Exception as e:
        print("Myntra API might have changed or failed.", str(e))
        return []


def aggregate_results(product_name, min_price, max_price, sites):
    results = []
    if "Amazon" in sites:
        results.extend(scrape_amazon(product_name, min_price, max_price))
    if "Flipkart" in sites:
        results.extend(scrape_flipkart(product_name, min_price, max_price))
    if "Myntra" in sites:
        results.extend(scrape_myntra(product_name, min_price, max_price))
    return sorted(results, key=lambda x: x['price'])
