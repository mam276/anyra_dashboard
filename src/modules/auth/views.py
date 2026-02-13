# src/modules/auth/views.py

import streamlit as st
from utils.session import login_user, signup_user, current_user

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
        user = login_user(email, password)
        if user:
            st.session_state["user"] = user
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
            user = login_user(email, password)
            if user:
                st.session_state["user"] = user
                st.success("Logged in successfully.")
            else:
                st.error("Invalid credentials.")
    else:
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            user = signup_user(name, email, password)
            if user:
                st.session_state["user"] = user
                st.success("Signup successful. Please login.")
    else:
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Signup"):
            user = signup_user(name, email, password)
            if user:

                st.success("Signup successful. Please login.")
