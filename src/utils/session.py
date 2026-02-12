import streamlit as st

def init_session():
    if "user" not in st.session_state:
        st.session_state["user"] = None

def login_user(email, password):
    if email == "admin@example.com" and password == "admin":
        return {"id":1,"name":"Admin","role":"admin","industry":"generic"}
    elif email == "client@example.com" and password == "client":
        return {"id":2,"name":"Client","role":"client","industry":"retail"}
    elif email == "viewer@example.com" and password == "viewer":
        return {"id":3,"name":"Viewer","role":"viewer","industry":"generic"}
    return None

def signup_user(name,email,password):
    return {"id":99,"name":name,"role":"client","industry":"generic"}

def current_user():
    return st.session_state.get("user")