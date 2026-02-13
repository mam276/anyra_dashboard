# src/modules/auth/views.py

import streamlit as st
from utils.session import (
    login_user as do_login,
    signup_user,
    current_user,
    forgot_password,
    reset_password
)

def login_user():
    """
    Wrapper to ensure login runs at app startup.
    Uses login_user from utils.session.
    """
    if st.session_state.get("authenticated"):
        return
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if do_login(email, password):
            st.session_state["authenticated"] = True
            st.success("Logged in successfully.")
        else:
            st.error("Invalid credentials.")

def show_auth():
    """
    Displays the Auth module UI when selected from the sidebar.
    """
    st.subheader("Authentication")
    choice = st.radio("Select", ["Login", "Signup"])
    if choice == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if do_login(email, password):
                st.session_state["authenticated"] = True
                st.success("Logged in successfully.")
            else:
                st.error("Invalid credentials.")
    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            if signup_user(email, password):
                st.success("Signup successful. Please login.")
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
