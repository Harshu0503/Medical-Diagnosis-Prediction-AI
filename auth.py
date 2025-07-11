import streamlit as st
import json
import os
from streamlit.components.v1 import html

USER_FILE = "users.json"

def load_users():
    """Load users from JSON file with error handling."""
    try:
        if not os.path.exists(USER_FILE):
            return {}
            
        if os.path.getsize(USER_FILE) == 0:
            return {}
            
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("Corrupted user data file. Resetting to empty.")
        return {}
    except Exception as e:
        st.error(f"Error loading user data: {e}")
        return {}

def save_users(users):
    """Save users to JSON file with error handling."""
    try:
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        st.error(f"Error saving user data: {e}")

def authenticate():
    """Handle user authentication with improved UI and interactivity."""
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.just_registered = False

    # If already authenticated, return True
    if st.session_state.authenticated:
        return True

    # Custom CSS for better styling
    st.markdown("""
    <style>
        .auth-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .auth-title {
            text-align: center;
            margin-bottom: 30px;
            color: #2c3e50;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            padding: 10px;
            font-weight: 500;
        }
        .stTextInput>div>div>input {
            padding: 10px;
        }
        .tab-content {
            padding: 20px 0;
        }
        .stAlert {
            animation: fadeIn 0.5s, fadeOut 0.5s 2.5s;
            animation-fill-mode: forwards;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    </style>
    """, unsafe_allow_html=True)

    # Main auth container
    with st.container():
        st.markdown('<h1 class="auth-title">🔐 Login / Register</h1>', unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2 = st.tabs(["Login", "Register"])
        users = load_users()

        # --- Login Tab ---
        with tab1:
            with st.form("login_form"):
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                login_btn = st.form_submit_button("Login")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if login_btn:
                    if not username or not password:
                        st.error("Both username and password are required.")
                    elif username in users and users[username]["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success(f"Welcome back, {users[username]['name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        # --- Register Tab ---
        with tab2:
            with st.form("register_form"):
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                
                full_name = st.text_input("Full Name", key="reg_name")
                new_username = st.text_input("Username", key="reg_user")
                new_password = st.text_input("Password", type="password", key="reg_pass")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
                register_btn = st.form_submit_button("Register")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                if register_btn:
                    if not all([full_name, new_username, new_password, confirm_password]):
                        st.warning("All fields are required.")
                    elif new_password != confirm_password:
                        st.warning("Passwords don't match!")
                    elif new_username in users:
                        st.warning("Username already exists. Choose another.")
                    else:
                        users[new_username] = {
                            "name": full_name,
                            "password": new_password  # Note: In production, use hashed passwords!
                        }
                        save_users(users)
                        st.session_state.just_registered = True
                        
                        # Show success message that will auto-close
                        success_placeholder = st.empty()
                        success_placeholder.success("🎉 Registration successful! Please log in using your new credentials.")
                        
                        # Auto-scroll to login tab after 1 second
                        html("""
                        <script>
                            setTimeout(function() {
                                const tabs = window.parent.document.querySelectorAll('[role="tab"]');
                                if (tabs && tabs.length > 0) {
                                    tabs[0].click();
                                }
                                
                                // Remove the success message after 3 seconds
                                setTimeout(function() {
                                    var alerts = window.parent.document.querySelectorAll('.stAlert');
                                    if (alerts && alerts.length > 0) {
                                        alerts[0].style.display = 'none';
                                    }
                                }, 3000);
                            }, 1000);
                        </script>
                        """)
                        st.rerun()

    # Show special message if user just registered
    if st.session_state.get('just_registered', False):
        with tab1:
            st.info("Please log in with your new credentials.")
            st.session_state.just_registered = False

    return False


# Example usage in your app
if __name__ == "__main__":
    if authenticate():
        st.title("Welcome to Medical Diagnosis System")
        st.write(f"Hello, {st.session_state.username}!")
        st.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "username": None}))
    else:
        st.write("Please authenticate to access the system.")
