# src/utils/session.py

import streamlit as st
import bcrypt
import secrets
import time
from utils.email import send_email  # assumes you have a send_email utility

# In-memory user store (replace with DB in production)
USERS = {}
RESET_TOKENS = {}

def signup_user(email: str, password: str, role: str = "user", subscription_level: str = "free"):
    """
    Register a new user with hashed password.
    """
    if email in USERS:
        return False
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    USERS[email] = {
        "password": hashed,
        "role": role,
        "subscription_level": subscription_level
    }
    return True

def login_user(email: str, password: str):
    """
    Verify login using hashed password.
    """
    user = USERS.get(email)
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        st.session_state["user"] = email
        st.session_state["role"] = user.get("role", "user")
        st.session_state["subscription_level"] = user.get("subscription_level", "free")
        return True
    return False

def current_user():
    """
    Return current logged-in user info.
    """
    email = st.session_state.get("user")
    if not email:
        return None
    return USERS.get(email)

def logout_user():
    """
    Clear session state.
    """
    st.session_state.pop("user", None)
    st.session_state.pop("role", None)
    st.session_state.pop("subscription_level", None)

# ---------------------------
# Forgot Password Flow
# ---------------------------

def forgot_password(email: str):
    """
    Generate a reset token if user exists and send email.
    """
    user = USERS.get(email)
    if user:
        token = secrets.token_urlsafe(16)
        RESET_TOKENS[token] = {"email": email, "expires": time.time() + 900}  # 15 min expiry
        send_reset_email(email, token)
        return True
    return False

def send_reset_email(email: str, token: str):
    """
    Send reset link via email.
    """
    reset_link = f"https://yourapp.streamlit.app/?page=reset&token={token}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n{reset_link}\nThis link expires in 15 minutes."
    send_email(email, subject, body)

def reset_password(token: str, new_password: str):
    """
    Reset password securely using token.
    """
    data = RESET_TOKENS.get(token)
    if data and time.time() < data["expires"]:
        email = data["email"]
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        USERS[email]["password"] = hashed
        del RESET_TOKENS[token]  # invalidate token
        return True
    return False

# ---------------------------
# RBAC & Subscription
# ---------------------------

def enforce_role(required_role: str):
    """
    Ensure current user has required role.
    """
    role = st.session_state.get("role", "user")
    return role == required_role

def enforce_subscription(required_level: str):
    """
    Ensure current user has required subscription level.
    """
    level = st.session_state.get("subscription_level", "free")
    return level == required_level
