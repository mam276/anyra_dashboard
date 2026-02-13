import streamlit as st
from utils.audit import log_action

CONTACTS = []

def show_crm_dashboard():
    st.title("CRM Dashboard")

    # Add new contact
    with st.form("add_contact"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        company = st.text_input("Company")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Contact")
        if submitted and name and email:
            CONTACTS.append({"name": name, "email": email, "company": company, "notes": notes})
            log_action(st.session_state.get("user", "guest"), f"added_contact:{email}")
            st.success(f"Contact {name} added!")

    # Show contacts
    if CONTACTS:
        st.subheader("Contacts")
        for c in CONTACTS:
            st.write(f"**{c['name']}** ({c['email']}) - {c['company']}")
            st.caption(c["notes"])
