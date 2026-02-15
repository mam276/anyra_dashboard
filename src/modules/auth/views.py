import streamlit as st
from utils.session import (
    login_user,
    signup_user,
    forgot_password,
    reset_password,
    restore_user,
    logout_user
)


# -----------------------------
#   AUTH SCREEN (LOGIN / SIGNUP / FORGOT)
# -----------------------------
def show_auth():
    st.title("Authentication")

    tabs = st.tabs(["Login", "Sign Up", "Forgot Password"])

    # ---------------- LOGIN ----------------
    with tabs[0]:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        remember = st.checkbox("Remember me", key="login_remember")

        if st.button("Login"):
            if login_user(email, password, remember):
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid email or password")

    # ---------------- SIGNUP ----------------
    with tabs[1]:
        st.subheader("Create an Account")

        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")

        if st.button("Sign Up"):
            if signup_user(email, password):
                st.success("Account created successfully. Please log in.")
            else:
                st.error("Email already exists")

    # ---------------- FORGOT PASSWORD ----------------
    with tabs[2]:
        st.subheader("Forgot Password")

        email = st.text_input("Enter your email", key="forgot_email")

        if st.button("Send Reset Link"):
            if forgot_password(email):
                st.success("Password reset link sent to your email.")
            else:
                st.error("Email not found")


# -----------------------------
#   RESET PASSWORD SCREEN
# -----------------------------
def show_reset_form(token: str):
    st.title("Reset Password")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Reset Password"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
            return

        if reset_password(token, new_password):
            st.success("Password reset successful. Please log in.")
            st.write("You can now close this page.")
        else:
            st.error("Invalid or expired reset link")
