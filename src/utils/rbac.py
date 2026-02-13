# src/utils/rbac.py

import streamlit as st

def enforce_role(required_role: str) -> bool:
    """
    Check if the current user has the required role.
    Returns True if the role matches, False otherwise.
    """
    return st.session_state.get("role") == required_role

def enforce_subscription(required_level: str) -> bool:
    """
    Check if the current user has the required subscription tier.
    Returns True if the subscription level matches, False otherwise.
    """
    return st.session_state.get("subscription_level") == required_level
