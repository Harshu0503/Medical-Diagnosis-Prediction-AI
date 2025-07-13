import streamlit as st
import json
import os

USER_FILE = "users.json"

def load_users():
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
    try:
        with open(USER_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        st.error(f"Error saving user data: {e}")

def authenticate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.just_registered = False

    if st.session_state.authenticated:
        return True

    users = load_users()

    st.title("AI-Powered Medical Diagnosis System")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Login")
            with st.form("login_form"):
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                login_btn = st.form_submit_button("Login")

                if login_btn:
                    if not username or not password:
                        st.error("Both fields are required.")
                    elif username in users and users[username]["password"] == password:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success(f"Welcome back, {users[username]['name']}!")
                        st.rerun()

                    else:
                        st.error("Invalid credentials.")

        with col2:
            st.markdown("### Welcome back!")
            st.write("Please login to continue to your medical dashboard.")

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Hello, New User")
            st.write("Please fill out the registration form.")

        with col2:
            st.subheader("Register")
            with st.form("register_form"):
                full_name = st.text_input("Full Name", key="reg_name")
                new_username = st.text_input("Username", key="reg_user")
                new_password = st.text_input("Password", type="password", key="reg_pass")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
                register_btn = st.form_submit_button("Register")

                if register_btn:
                    if not all([full_name, new_username, new_password, confirm_password]):
                        st.warning("All fields are required.")
                    elif new_password != confirm_password:
                        st.warning("Passwords do not match.")
                    elif new_username in users:
                        st.warning("Username already exists.")
                    else:
                        users[new_username] = {
                            "name": full_name,
                            "password": new_password  # Use hashed passwords in production
                        }
                        save_users(users)
                        st.success("Registration successful! Please log in.")
                        st.session_state.just_registered = True
                        st.rerun()


    return False

if __name__ == "__main__":
    st.set_page_config(page_title="Medical Diagnosis Login", layout="centered")

    if authenticate():
        st.title("🏥 Welcome to the Medical Diagnosis System")
        st.success(f"Hello, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

