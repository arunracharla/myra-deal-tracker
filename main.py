import streamlit as st
from myra_chat import get_user_preferences, greet_user
from tracker import check_deals
import os

st.set_page_config(page_title="Myra – Smart Deal Tracker", layout="centered")

if "products" not in st.session_state:
    st.session_state.products = []

st.title("🛍️ Myra – Your Personal Deal Tracker")

greet_user()

# Step 1: Take input
with st.form("deal_form"):
    product_name = st.text_input("Enter the product you want to track", "")
    min_price = st.number_input("Minimum Price ₹", min_value=0)
    max_price = st.number_input("Maximum Price ₹", min_value=0)
    preferred_sites = st.multiselect("Preferred Sites", ["Amazon", "Flipkart"])
    category = st.selectbox("Category", ["Electronics", "Home", "Fashion", "Other"])
    phone_number = st.text_input("Your WhatsApp Number (e.g. +919012345678)", "")
    submitted = st.form_submit_button("Add this to Myra's memory")

    if submitted:
        st.session_state.products.append({
            "product": product_name,
            "min_price": min_price,
            "max_price": max_price,
            "sites": preferred_sites,
            "category": category,
            "phone": phone_number
        })
        st.success(f"Myra is now tracking '{product_name}'!")

# Step 2: Show tracked items
if st.session_state.products:
    st.markdown("### 📋 Currently Tracked:")
    for idx, item in enumerate(st.session_state.products):
        st.markdown(f"- {item['product']} ({item['min_price']}–{item['max_price']} ₹) on {', '.join(item['sites'])}")

# Step 3: Run tracking
if st.button("🔍 Run Deal Check Now"):
    st.info("Checking the universe for best deals... 🛰️")
    for product in st.session_state.products:
        matched = check_deals(product)
        if matched:
            st.success(f"✅ Found Deal for: {product['product']}")
        else:
            st.warning(f"❌ No deals found yet for: {product['product']}")
