# src/utils/session.py

import streamlit as st

# In-memory "database" for demo purposes
USERS = {}

def init_session():
    """
    Initialize session state variables if not already set.
    """
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "role" not in st.session_state:
        st.session_state["role"] = "user"
    if "subscription_level" not in st.session_state:
        st.session_state["subscription_level"] = "free"
    if "tenant_id" not in st.session_state:
        st.session_state["tenant_id"] = None

def login_user(email: str, password: str):
    """
    Validate user credentials. Returns user dict if valid, else None.
    """
    init_session()
    user = USERS.get(email)
    if user and user["password"] == password:
        st.session_state["authenticated"] = True
        st.session_state["user"] = {"name": user["name"], "email": email}
        return st.session_state["user"]
    return None

def signup_user(name: str, email: str, password: str):
    """
    Register a new user. Returns user dict.
    """
    init_session()
    if email in USERS:
        return None  # already exists
    USERS[email] = {"name": name, "password": password}
    st.session_state["authenticated"] = True
    st.session_state["user"] = {"name": name, "email": email}
    return st.session_state["user"]

def current_user():
    """
    Return the current logged-in user dict, or None.
    """
    return st.session_state.get("user")
