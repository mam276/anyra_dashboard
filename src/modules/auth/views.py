import streamlit as st
from utils.session import login_user, signup_user, forgot_password, reset_password, restore_user

def show_auth():
    st.title("Anyra Dashboard – Access")

    # Try auto-restore
    restore_user()
    if st.session_state.get("user"):
        st.success(f"Welcome back, {st.session_state['user']['email']}!")
        return

    tab_login, tab_signup, tab_forgot = st.tabs(["Login", "Sign Up", "Forgot Password"])

    with tab_login:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        remember_me = st.checkbox("Remember Me", key="remember_me")
        if st.button("Login", key="login_button"):
            if login_user(email, password, remember_me=remember_me):
                st.success("Logged in successfully.")
                st.rerun()
            else:
                st.error("Invalid credentials.")

    with tab_signup:
        st.subheader("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_button"):
            if signup_user(email, password):
                st.success("Signup successful. Please log in.")
                st.rerun()
            else:
                st.error("Email already exists.")

    with tab_forgot:
        st.subheader("Forgot Password")
        email = st.text_input("Enter your registered email", key="forgot_email")
        if st.button("Send Reset Link", key="forgot_button"):
            if forgot_password(email):
                st.success("Password reset link sent to your email.")
            else:
                st.error("Email not found.")
