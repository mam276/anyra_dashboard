import streamlit as st
from utils.session import (
    login_user as do_login,
    signup_user,
    current_user,
    forgot_password,
    reset_password
)

def show_auth():
    """
    Unified authentication screen with Login and Signup tabs.
    Uses backend functions from utils.session.
    """
    st.title("Anyra Dashboard – Access")

    # Tabs for Login and Signup
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    # ---------------------------
    # Login Tab
    # ---------------------------
    with tab_login:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if do_login(email, password):
                st.session_state["authenticated"] = True
                st.success("Logged in successfully.")
            else:
                st.error("Invalid credentials.")

    # ---------------------------
    # Signup Tab
    # ---------------------------
    with tab_signup:
        st.subheader("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_button"):
            if signup_user(email, password):
                st.success("Signup successful. Please log in.")
            else:
                st.error("Email already exists.")

def show_forgot_password():
    """
    UI for forgot password flow.
    """
    st.subheader("Forgot Password")
    email = st.text_input("Enter your registered email")
    if st.button("Send Reset Link"):
        if forgot_password(email):
            st.success("Password reset link sent to your email.")
        else:
            st.error("Email not found.")

def show_reset_form(token: str):
    """
    UI for resetting password via token link.
    """
    st.subheader("Reset Your Password")
    new_password = st.text_input("Enter new password", type="password")
    if st.button("Reset Password"):
        if reset_password(token, new_password):
            st.success("Password reset successful. Please login.")
        else:
            st.error("Invalid or expired reset link.")
