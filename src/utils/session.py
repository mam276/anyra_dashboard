# src/utils/session.py

import streamlit as st

def init_session():
    defaults = {
        "authenticated": False,
        "role": "guest",
        "subscription_level": "none",
        "tenant_id": None,
        "user": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def login_user(email: str, password: str):
    """
    Authenticate user by email/password.
    Returns a user dict if valid, else None.
    Also updates st.session_state with RBAC values.
    """
    if email == "admin@example.com" and password == "admin":
        user = {"id": 1, "name": "Admin", "role": "admin", "industry": "generic"}
        st.session_state.authenticated = True
        st.session_state.role = "admin"
        st.session_state.subscription_level = "premium"
        st.session_state.tenant_id = "global_admin"
        return user

    elif email == "client@example.com" and password == "client":
        user = {"id": 2, "name": "Client", "role": "client", "industry": "retail"}
        st.session_state.authenticated = True
        st.session_state.role = "user"
        st.session_state.subscription_level = "premium"
        st.session_state.tenant_id = "tenant_A"
        return user

    elif email == "viewer@example.com" and password == "viewer":
        user = {"id": 3, "name": "Viewer", "role": "viewer", "industry": "generic"}
        st.session_state.authenticated = True
        st.session_state.role = "viewer"
        st.session_state.subscription_level = "basic"
        st.session_state.tenant_id = "tenant_B"
        return user

    return None

def signup_user(name: str, email: str, password: str):
    """
    Demo signup logic — replace with DB insert.
    Returns a new user dict.
    """
    user = {"id": 99, "name": name, "role": "client", "industry": "generic"}
    # By default, signup gives a basic subscription
    st.session_state.authenticated = True
    st.session_state.role = "user"
    st.session_state.subscription_level = "basic"
    st.session_state.tenant_id = "tenant_new"
    return user

def current_user():
    return st.session_state.get("user")
