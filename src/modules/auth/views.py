import streamlit as st
from utils.session import (
    login_user as do_login,
    signup_user,
    forgot_password,
    reset_password
)

def show_auth():
    """
    Unified authentication screen with Login, Signup, and Forgot Password tabs.
    """
    st.title("Anyra Dashboard – Access")

    tab_login, tab_signup, tab_forgot = st.tabs(["Login", "Sign Up", "Forgot Password"])

    # ---------------------------
    # Login Tab
    # ---------------------------
    with tab_login:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if not email or not password:
                st.error("Email and password are required.")
            elif do_login(email, password):
                st.session_state["user"] = {"email": email}
                st.success("Logged in successfully.")
                st.experimental_rerun()
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
            if not email or not password:
                st.error("Email and password are required.")
            elif "@" not in email:
                st.error("Please enter a valid email address.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            elif signup_user(email, password):
                st.success("Signup successful. Please log in.")
            else:
                st.error("Email already exists.")

    # ---------------------------
    # Forgot Password Tab
    # ---------------------------
    with tab_forgot:
        st.subheader("Forgot Password")
        email = st.text_input("Enter your registered email", key="forgot_email")
        if st.button("Send Reset Link", key="forgot_button"):
            if not email:
                st.error("Email is required.")
            elif forgot_password(email):
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
        if not new_password:
            st.error("Password is required.")
        elif len(new_password) < 8:
            st.error("Password must be at least 8 characters long.")
        elif reset_password(token, new_password):
            st.success("Password reset successful. Please login.")
        else:
            st.error("Invalid or expired reset link.")
