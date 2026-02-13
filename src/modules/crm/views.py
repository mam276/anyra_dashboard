import streamlit as st
from utils.audit import log_action

CONTACTS = []
LEADS = []

def show_crm_dashboard():
    st.title("CRM Dashboard")

    # Tabs for Contacts and Leads
    tab1, tab2 = st.tabs(["Contacts", "Leads & Opportunities"])

    # ---------------------------
    # Contacts Tab
    # ---------------------------
    with tab1:
        st.subheader("Manage Contacts")

        with st.form("add_contact"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            company = st.text_input("Company")
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Contact")
            if submitted and name and email:
                CONTACTS.append({
                    "name": name,
                    "email": email,
                    "company": company,
                    "notes": notes
                })
                log_action(st.session_state.get("user", "guest"), f"added_contact:{email}")
                st.success(f"Contact {name} added!")

        if CONTACTS:
            st.subheader("Contacts List")
            for c in CONTACTS:
                st.write(f"**{c['name']}** ({c['email']}) - {c['company']}")
                st.caption(c["notes"])

    # ---------------------------
    # Leads & Opportunities Tab
    # ---------------------------
    with tab2:
        st.subheader("Track Leads & Opportunities")

        with st.form("add_lead"):
            lead_name = st.text_input("Lead Name")
            company = st.text_input("Company")
            stage = st.selectbox(
                "Stage",
                ["Prospect", "Qualified", "Proposal Sent", "Negotiation", "Closed Won", "Closed Lost"]
            )
            value = st.number_input("Deal Value ($)", min_value=0.0, step=100.0)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Add Lead")
            if submitted and lead_name:
                LEADS.append({
                    "lead_name": lead_name,
                    "company": company,
                    "stage": stage,
                    "value": value,
                    "notes": notes
                })
                log_action(st.session_state.get("user", "guest"), f"added_lead:{lead_name}")
                st.success(f"Lead {lead_name} added!")

        if LEADS:
            st.subheader("Pipeline Overview")
            for l in LEADS:
                st.write(f"**{l['lead_name']}** ({l['company']}) - Stage: {l['stage']} - Value: ${l['value']}")
                st.caption(l["notes"])
