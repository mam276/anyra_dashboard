import streamlit as st
from utils.session import login_user, signup_user

def show_auth():
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
                st.success("Signup successful. Please login.")