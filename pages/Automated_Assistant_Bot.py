import streamlit as st
from google_ai_services import answer_customer_query

st.set_page_config(page_title="Assistant Bot", page_icon="🤖")
st.title("🤖 Automated Assistant Bot")

if not st.session_state.get('logged_in'):
    st.warning("Please log in from the Artisan Dashboard first.")
else:
    st.info("Test how the AI assistant will answer customer questions about your products. It uses your profile story, product details, and the chat history for context.")
    
    products = st.session_state.profile.get("products", {})
    if not products:
        st.warning("You have no products to test. Please add a product first.")
    else:
        product_options = {p_id: p_data['name'] for p_id, p_data in products.items()}
        selected_product_id = st.selectbox(
            "Select one of your products to test:", 
            options=list(product_options.keys()), 
            format_func=lambda x: product_options[x],
            key="product_select" # Add a key to track this widget
        )

        # --- NEW: Logic to clear chat history when product changes ---
        if 'current_product_id' not in st.session_state:
            st.session_state.current_product_id = selected_product_id
        
        if st.session_state.current_product_id != selected_product_id:
            st.session_state.messages = [] # Clear previous chat
            st.session_state.current_product_id = selected_product_id
            st.rerun() # Refresh the page to show the cleared chat

        # --- Standard Chatbot UI ---
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a follow-up question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.spinner("Sahayak Bot is thinking..."):
                artisan_context = st.session_state.profile.get('art_description', '')
                product_details = products[selected_product_id]
                
                # --- THIS IS THE KEY CHANGE ---
                # Send the entire chat history, not just the last prompt
                response = answer_customer_query(artisan_context, product_details, st.session_state.messages)
                
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})