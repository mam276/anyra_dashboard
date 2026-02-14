import streamlit as st
import bcrypt
import secrets
import time
from utils.email import send_email
from utils.audit import log_event
from utils.db import SessionLocal, User

RESET_TOKENS = {}

def signup_user(email: str, password: str, role: str = "user", subscription_level: str = "free"):
    """Register a new user with hashed password in DB."""
    db = SessionLocal()
    existing = db.query(User).filter_by(email=email).first()
    if existing:
        db.close()
        return False
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = User(email=email, password_hash=hashed, role=role, subscription=subscription_level)
    db.add(user)
    db.commit()
    db.close()
    log_event(email, "signup")
    return True

def login_user(email: str, password: str):
    """Verify login using DB."""
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    db.close()
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        st.session_state["user"] = {
            "id": user.id,
            "email": email,
            "role": user.role,
            "subscription": user.subscription
        }
        log_event(email, "login")
        return True
    log_event(email, "failed_login")
    return False

def current_user():
    """Return current logged-in user info from session_state."""
    return st.session_state.get("user")

def logout_user():
    """Clear session state and log logout."""
    user = st.session_state.get("user")
    st.session_state.clear()
    if user:
        log_event(user.get("email"), "logout")

def forgot_password(email: str):
    """Generate a reset token if user exists and send email."""
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    db.close()
    if user:
        token = secrets.token_urlsafe(16)
        RESET_TOKENS[token] = {"email": email, "expires": time.time() + 900}
        send_reset_email(email, token)
        log_event(email, "forgot_password_request")
        return True
    return False

def send_reset_email(email: str, token: str):
    reset_link = f"https://yourapp.streamlit.app/?page=reset&token={token}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n{reset_link}\nThis link expires in 15 minutes."
    send_email(email, subject, body)

def reset_password(token: str, new_password: str):
    """Reset password securely using token."""
    data = RESET_TOKENS.get(token)
    if data and time.time() < data["expires"]:
        email = data["email"]
        db = SessionLocal()
        user = db.query(User).filter_by(email=email).first()
        if user:
            hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user.password_hash = hashed
            db.commit()
            db.close()
            del RESET_TOKENS[token]
            log_event(email, "password_reset")
            return True
    return False

def enforce_role(required_role: str):
    role = st.session_state.get("role", "user")
    if role != required_role:
        log_event(st.session_state.get("user", {}).get("email", "anonymous"), f"role_denied:{required_role}")
    return role == required_role

def enforce_subscription(required_level: str):
    level = st.session_state.get("subscription", "free")
    if level != required_level:
        log_event(st.session_state.get("user", {}).get("email", "anonymous"), f"subscription_denied:{required_level}")
    return level == required_level

def init_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "subscription" not in st.session_state:
        st.session_state["subscription"] = "free"
    if "role" not in st.session_state:
        st.session_state["role"] = "guest"
    if "popup_shown" not in st.session_state:
        st.session_state["popup_shown"] = False
    if "tip_shown" not in st.session_state:
        st.session_state["tip_shown"] = False
    if "tour_completed" not in st.session_state:
        st.session_state["tour_completed"] = False
