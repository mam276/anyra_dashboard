# src/utils/session.py

import streamlit as st
import bcrypt

# In-memory user store (replace with DB in production)
USERS = {}

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

def forgot_password(email: str):
    """
    Demo forgot password: return True if user exists.
    In production: generate token and send email.
    """
    return email in USERS

def reset_password(email: str, new_password: str):
    """
    Reset password securely with hashing.
    """
    user = USERS.get(email)
    if user:
        hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        user["password"] = hashed
        return True
    return False

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
