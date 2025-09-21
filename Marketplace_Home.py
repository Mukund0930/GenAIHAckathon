import streamlit as st
import json
from google_ai_services import translate_text # Import the translation function

# --- Page Configuration ---
st.set_page_config(
    page_title="KalaKriti Marketplace",
    page_icon="🏠",
    layout="wide"
)

# --- Database Function ---
def load_db():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# --- Language Selection & State Management ---
st.sidebar.header(translate_text("Language Selection", st.session_state.get('language', 'en')))
languages = {"English": "en", "Hindi": "hi", "Gujarati": "gu"}
selected_lang_name = st.sidebar.selectbox(
    translate_text("Choose a language:", st.session_state.get('language', 'en')),
    languages.keys()
)

# Store the chosen language code (e.g., 'hi') in the session state
if 'language' not in st.session_state or st.session_state['language'] != languages[selected_lang_name]:
    st.session_state['language'] = languages[selected_lang_name]
    st.rerun() # Rerun the app to apply the new language

# Get the current language for this run
lang = st.session_state.get('language', 'en')

# --- Main Page Content ---
st.title(translate_text("KalaKriti AI Marketplace", lang))
st.markdown(translate_text("Discover unique, handcrafted treasures from the heart of India.", lang))

db = load_db()
all_products = []

# Aggregate all products from all artisans
for username, data in db.items():
    if "products" in data:
        for product_id, product_details in data["products"].items():
            # Attach artisan info to each product for easy access
            product_details['artisan_name'] = data.get('name', username)
            product_details['artisan_story'] = data.get('art_description', 'No story provided.')
            product_details['product_id'] = product_id
            all_products.append(product_details)

# --- Search and Filter ---
search_query = st.text_input(translate_text("Search for a craft or product", lang), "")
if search_query:
    all_products = [p for p in all_products if search_query.lower() in p['name'].lower() or search_query.lower() in p.get('craft_type', '').lower()]

# --- Display Products ---
if not all_products:
    st.info(translate_text("No products found. Artisans, please log in to add your creations!", lang))
else:
    # Create a grid of 3 columns
    cols = st.columns(3)
    for i, product in enumerate(all_products):
        col = cols[i % 3]
        with col:
            with st.container(border=True):
                # Display product details, translating each piece of text
                st.subheader(translate_text(product['name'], lang))
                st.caption(f"{translate_text('by', lang)} {translate_text(product['artisan_name'], lang)}")
                
                # In a real app, you would display an image here:
                # st.image(product['image_url']) 
                st.info(f"{translate_text('Price', lang)}: ₹{product['price']:.2f}")

                with st.expander(translate_text("View Details & Artisan's Story", lang)):
                    st.markdown(f"**{translate_text('About this item:', lang)}**")
                    st.write(translate_text(product.get('description_story', 'No description available.'), lang))
                    
                    st.markdown(f"**{translate_text('Features:', lang)}**")
                    st.write(translate_text(product.get('description_bullets', ''), lang))
                    
                    st.divider()
                    st.markdown(f"**{translate_text('The Story of', lang)} {translate_text(product['artisan_name'], lang)}**")
                    st.write(translate_text(product['artisan_story'], lang))