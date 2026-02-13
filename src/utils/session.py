# src/utils/session.py

import streamlit as st
import bcrypt
import secrets
import time
from utils.email import send_email
from utils.audit import log_action

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
    log_action(email, "signup")
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
        log_action(email, "login")
        return True
    log_action(email, "failed_login")
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
    Clear session state and log logout.
    """
    email = st.session_state.get("user")
    st.session_state.pop("user", None)
    st.session_state.pop("role", None)
    st.session_state.pop("subscription_level", None)
    if email:
        log_action(email, "logout")

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
        log_action(email, "forgot_password_request")
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
        log_action(email, "password_reset")
        return True
    return False

# ---------------------------
# RBAC & Subscription
# ---------------------------

def enforce_role(required_role: str):
    """
    Ensure current user has required role.
    Logs denied attempts.
    """
    role = st.session_state.get("role", "user")
    if role != required_role:
        log_action(st.session_state.get("user", "anonymous"), f"role_denied:{required_role}")
    return role == required_role

def enforce_subscription(required_level: str):
    """
    Ensure current user has required subscription level.
    Logs denied attempts.
    """
    level = st.session_state.get("subscription_level", "free")
    if level != required_level:
        log_action(st.session_state.get("user", "anonymous"), f"subscription_denied:{required_level}")
    return level == required_level

def init_session():
    """
    Initialize Streamlit session state with defaults.
    Ensures required keys exist before the app runs.
    """
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "subscription_level" not in st.session_state:
        st.session_state["subscription_level"] = "free"
    if "role" not in st.session_state:
        st.session_state["role"] = "guest"
    if "popup_shown" not in st.session_state:
        st.session_state["popup_shown"] = False
    if "tip_shown" not in st.session_state:
        st.session_state["tip_shown"] = False
    if "tour_completed" not in st.session_state:
        st.session_state["tour_completed"] = False
