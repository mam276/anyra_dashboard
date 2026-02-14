import streamlit as st
import bcrypt
import secrets
import time
from utils.email import send_email
from utils.audit import log_event
from utils.db import SessionLocal, User

RESET_TOKENS = {}

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

def restore_user():
    """Restore user from DB if a remember_token exists."""
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

def current_user():
    return st.session_state.get("user")

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
