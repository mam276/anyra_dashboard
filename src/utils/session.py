import streamlit as st
import bcrypt
import secrets
import time
from utils.email import send_email
from utils.audit import log_event
from utils.db import SessionLocal, User

RESET_TOKENS = {}


# -----------------------------
#   SIGNUP
# -----------------------------
def signup_user(email: str, password: str, role: str = "user", subscription_level: str = "free"):
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


# -----------------------------
#   LOGIN
# -----------------------------
def login_user(email: str, password: str, remember_me: bool = False):
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()

    if user and bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        st.session_state["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "subscription": user.subscription
        }

        if remember_me:
            token = secrets.token_urlsafe(32)
            st.session_state["remember_token"] = token
            user.remember_token = token
            db.commit()

        log_event(email, "login")
        db.close()
        return True

    db.close()
    log_event(email, "failed_login")
    return False


# -----------------------------
#   RESTORE USER (Remember Me)
# -----------------------------
def restore_user():
    token = st.session_state.get("remember_token")
    if not token:
        return None

    db = SessionLocal()
    user = db.query(User).filter_by(remember_token=token).first()
    db.close()

    if user:
        st.session_state["user"] = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "subscription": user.subscription
        }
        return st.session_state["user"]

    return None


# -----------------------------
#   CURRENT USER
# -----------------------------
def current_user():
    return st.session_state.get("user")


# -----------------------------
#   LOGOUT
# -----------------------------
def logout_user():
    user = st.session_state.get("user")
    token = st.session_state.get("remember_token")

    if token:
        db = SessionLocal()
        db_user = db.query(User).filter_by(remember_token=token).first()
        if db_user:
            db_user.remember_token = None
            db.commit()
        db.close()

    st.session_state.clear()

    if user:
        log_event(user.get("email"), "logout")


# -----------------------------
#   FORGOT PASSWORD
# -----------------------------
def forgot_password(email: str):
    """Generate a reset token and send email."""
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    db.close()

    if not user:
        return False

    token = secrets.token_urlsafe(32)
    RESET_TOKENS[token] = {
        "email": email,
        "expires": time.time() + 3600  # 1 hour expiry
    }

    reset_link = f"{st.secrets.get('APP_URL', '')}?page=reset&token={token}"
    send_email(email, "Password Reset Request", f"Click here to reset your password: {reset_link}")

    log_event(email, "forgot_password")
    return True


# -----------------------------
#   RESET PASSWORD
# -----------------------------
def reset_password(token: str, new_password: str):
    """Validate token and update password."""
    data = RESET_TOKENS.get(token)

    if not data:
        return False

    if time.time() > data["expires"]:
        del RESET_TOKENS[token]
        return False

    email = data["email"]

    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()

    if not user:
        db.close()
        return False

    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user.password_hash = hashed
    db.commit()
    db.close()

    del RESET_TOKENS[token]

    log_event(email, "password_reset")
    return True


# -----------------------------
#   INIT SESSION
# -----------------------------
def init_session():
    """Initialize session defaults."""
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "remember_token" not in st.session_state:
        st.session_state["remember_token"] = None
