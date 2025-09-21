import streamlit as st
import json
import uuid
from google_ai_services import generate_product_descriptions

st.set_page_config(page_title="Add Product", page_icon="➕")
st.title("➕ Add a New Product to Your Store")

# --- Database Utility Functions ---
def load_db():
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_db(db):
    with open('database.json', 'w') as f:
        json.dump(db, f, indent=4)

# --- Main App Logic ---
if not st.session_state.get('logged_in'):
    st.warning("Please log in from the Artisan Dashboard first.")
else:
    artisan_context = st.session_state.profile.get('art_description')
    if not artisan_context or not st.session_state.profile.get('name'):
        st.error("Please complete your Artisan Profile first! The AI needs your story to create meaningful descriptions.")
    else:
        # Initialize session state for text areas
        if 'current_story' not in st.session_state:
            st.session_state.current_story = ""
        if 'current_bullets' not in st.session_state:
            st.session_state.current_bullets = ""
        if 'current_social' not in st.session_state:
            st.session_state.current_social = ""

        # --- Form for Product Details & AI Generation ---
        with st.form("product_details_form"):
            st.subheader("1. Product Details")
            product_name = st.text_input("Product Name")
            price = st.number_input("Price (INR)", min_value=0.0, format="%.2f")
            materials = st.text_input("Main Materials Used")
            
            submitted_generate = st.form_submit_button("Generate AI Suggestions", type="primary", help="The AI will use your profile story and product details to write descriptions.")
            
            if submitted_generate:
                if product_name and materials:
                    with st.spinner("Gemini is crafting descriptions for you..."):
                        descriptions = generate_product_descriptions(artisan_context, product_name, materials)
                        st.session_state['ai_descriptions'] = descriptions
                        
                        if "error" not in descriptions:
                            st.session_state.current_story = descriptions.get('story_driven', '')
                            
                            # --- THIS IS THE FIX FOR THE TypeError ---
                            # It converts the list of bullet points into a single string with newlines.
                            bullet_list = descriptions.get('bullet_points', [])
                            st.session_state.current_bullets = "\n".join(f"- {item}" for item in bullet_list)
                            # --- END FIX ---
                            
                            st.session_state.current_social = descriptions.get('social_media_caption', '')
                else:
                    st.warning("Please provide a Product Name and Materials.")

        # --- Error Handling and Suggestion Display ---
        if 'ai_descriptions' in st.session_state:
            descriptions = st.session_state.ai_descriptions
            
            if "error" in descriptions:
                st.error(f"**API Error:** {descriptions['error']}")
            else:
                st.subheader("2. AI Suggestions (Click 'Use' to apply)")
                
                # Callback functions to update the final text areas
                def use_story():
                    st.session_state.current_story = descriptions.get('story_driven', '')
                def use_bullets():
                    bullet_list = descriptions.get('bullet_points', [])
                    st.session_state.current_bullets = "\n".join(f"- {item}" for item in bullet_list) # Apply fix here too
                def use_social():
                    st.session_state.current_social = descriptions.get('social_media_caption', '')

                # UI for displaying suggestions and "Use" buttons
                with st.container(border=True):
                    st.markdown("**Story-Driven Suggestion:**")
                    st.write(descriptions.get('story_driven', ''))
                    st.button("Use this Story", on_click=use_story, key="use_story_btn")

                with st.container(border=True):
                    st.markdown("**Bulleted Features Suggestion:**")
                    for item in descriptions.get('bullet_points', []):
                        st.write(f"- {item}")
                    st.button("Use these Features", on_click=use_bullets, key="use_bullets_btn")

                with st.container(border=True):
                    st.markdown("**Social Media Caption Suggestion:**")
                    st.write(descriptions.get('social_media_caption', ''))
                    st.button("Use this Caption", on_click=use_social, key="use_social_btn")

        st.divider()

        # --- Final Editable Form and Save Button ---
        st.subheader("3. Final Descriptions (Edit here before saving)")
        with st.form("save_product_form"):
            st.text_area("Story-Driven Description", key="current_story", height=150)
            st.text_area("Bulleted Features", key="current_bullets", height=150)
            st.text_area("Social Media Caption", key="current_social", height=100)

            if st.form_submit_button("Add Product to Store", type="primary"):
                if product_name and price and st.session_state.current_story:
                    db = load_db()
                    username = st.session_state['username']
                    product_id = str(uuid.uuid4())
                    
                    if "products" not in db[username]:
                        db[username]["products"] = {}

                    db[username]["products"][product_id] = {
                        "name": product_name,
                        "price": price,
                        "materials": materials,
                        "description_story": st.session_state.current_story,
                        "description_bullets": st.session_state.current_bullets,
                        "description_social": st.session_state.current_social,
                        "craft_type": st.session_state.profile.get('craft', '')
                    }
                    save_db(db)
                    st.session_state['profile'] = db[username]
                    st.success(f"'{product_name}' has been added to your store!")
                    
                    keys_to_delete = ['ai_descriptions', 'current_story', 'current_bullets', 'current_social']
                    for key in keys_to_delete:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
                else:
                    st.error("Please ensure Product Name, Price, and the Story-Driven Description are filled out.")