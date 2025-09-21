import streamlit as st
import json
# The function name is generate_social_media_plan
from google_ai_services import generate_social_media_plan 

st.set_page_config(page_title="AI Post Planner", page_icon="🗓️")
st.title("🗓️ AI Post Planner")

if not st.session_state.get('logged_in'):
    st.warning("Please log in from the Artisan Dashboard first.")
else:
    artisan_context = st.session_state.profile.get('art_description')
    if not artisan_context or not st.session_state.profile.get('name'):
        st.error("Please complete your Artisan Profile first! The AI needs your story to create a meaningful plan.")
    else:
        st.info("This tool will generate a complete 3-day social media plan to help you market your products effectively.")

        # --- Inputs for the Planner ---
        with st.form("planner_inputs"):
            st.subheader("1. Tell the AI about your goal")
            # In a real app, the uploaded image would be analyzed by a vision model.
            # For this prototype, we'll just use its name for context.
            st.file_uploader("Upload a photo of your feature product (optional)", type=['png', 'jpg', 'jpeg'])
            product_name = st.text_input("Product Name", help="e.g., 'Ocean Blue Silk Saree'")
            campaign_goal = st.selectbox("What is the goal of this campaign?",
                                         options=[
                                             "Launch a new product",
                                             "Share the 'behind-the-scenes' making process",
                                             "Announce a weekend sale or special offer",
                                             "Educate customers about my unique craft",
                                             "Tell a story about a specific design"
                                         ])
            
            submitted = st.form_submit_button("Generate Content Plan", type="primary")

        # --- Display the Content Plan ---
        if submitted:
            if not product_name:
                st.warning("Please provide a product name.")
            else:
                with st.spinner("Your AI strategist is building your plan... 🧠"):
                    # Use the correct function name here as well
                    plan = generate_social_media_plan(artisan_context, product_name, campaign_goal) 
                    st.session_state['content_plan'] = plan
        
        if 'content_plan' in st.session_state:
            plan_data = st.session_state['content_plan']
            if "error" in plan_data:
                st.error(f"Could not generate plan: {plan_data['error']}")
            else:
                st.divider()
                st.header(plan_data.get('plan_title', "Your Content Plan"))

                for i, post in enumerate(plan_data.get('posts', [])):
                    with st.container(border=True):
                        st.subheader(post.get('day_title', f"Post {i+1}"))
                        
                        cols = st.columns([1, 2])
                        with cols[0]:
                            st.markdown("**Suggested Image:**")
                            st.info(post.get('suggested_image', ''))
                        
                        with cols[1]:
                            st.markdown("**Generated Caption:**")
                            # Using st.code makes it easy to copy the text
                            st.code(post.get('caption', ''), language=None)