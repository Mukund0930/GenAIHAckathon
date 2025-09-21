import streamlit as st
import json
import hashlib # Import the library for hashing passwords

st.set_page_config(page_title="Artisan Dashboard", page_icon="👤")

# --- Utility Functions ---
def load_db():
    """Loads the user database from the JSON file."""
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_db(db):
    """Saves the user database to the JSON file."""
    with open('database.json', 'w') as f:
        json.dump(db, f, indent=4)

def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Main Page Title ---
st.title("👤 Artisan Dashboard")

# --- Initialize Session State ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'profile' not in st.session_state:
    st.session_state['profile'] = {}

# --- Login / Registration Logic ---
if not st.session_state['logged_in']:
    
    # Let the user choose between logging in and registering
    choice = st.radio("Choose an action:", ["Login", "Register"], horizontal=True)

    if choice == "Login":
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                db = load_db()
                if username in db and db[username]['password_hash'] == hash_password(password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['profile'] = db[username]
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    elif choice == "Register":
        st.subheader("Create a New Account")
        with st.form("register_form"):
            username = st.text_input("Choose a unique username")
            password = st.text_input("Choose a password", type="password")
            
            if st.form_submit_button("Register"):
                db = load_db()
                if not username or not password:
                    st.warning("Please enter both a username and a password.")
                elif username in db:
                    st.error("This username is already taken. Please choose another one.")
                else:
                    # Create the new user profile with a hashed password
                    db[username] = {
                        "password_hash": hash_password(password),
                        "name": "", 
                        "craft": "", 
                        "art_description": "", 
                        "products": {}
                    }
                    save_db(db)
                    st.success("Registration successful! You can now log in.")
                    st.info("Please go to the Login tab to access your new dashboard.")

else:
    # --- This is the view for a Logged-in Artisan ---
    st.header(f"Welcome, {st.session_state.profile.get('name', st.session_state.username)}!")

    # --- Profile Editor ---
    with st.expander("Edit Your Artisan Profile & Story", expanded=True):
        with st.form("profile_form"):
            profile = st.session_state.get('profile', {})
            name = st.text_input("Your Full Name or Brand Name", value=profile.get('name', ''))
            craft = st.text_input("Name of Your Craft", value=profile.get('craft', ''))
            art_description = st.text_area("Your Story (The AI will use this!)", height=150, value=profile.get('art_description', ''))

            if st.form_submit_button("Save Profile"):
                db = load_db()
                username = st.session_state['username']
                # Update profile but keep the password hash
                db[username].update({"name": name, "craft": craft, "art_description": art_description})
                save_db(db)
                st.session_state['profile'] = db[username] # Refresh the profile in session
                st.success("Profile saved!")
                st.rerun()

    # --- Product Management ---
    st.subheader("Your Listed Products")
    products = st.session_state.profile.get("products", {})
    if not products:
        st.info("You haven't listed any products yet. Go to the 'Add New Product' page to get started!")
    else:
        for product_id, product_data in products.items():
            st.markdown(f"- **{product_data['name']}** (Price: ₹{product_data['price']})")
    
    # --- Logout Button ---
    if st.button("Logout"):
        # Clear all session data to log the user out
        st.session_state.clear() 
        st.rerun()