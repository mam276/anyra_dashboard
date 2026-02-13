import streamlit as st
import json
import os

LOG_FILE = "logs/audit.log"

def show_audit_dashboard():
    st.subheader("Audit Dashboard 📜")

    if not os.path.exists(LOG_FILE):
        st.warning("No audit logs found yet.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    events = []
    for line in lines[-200:]:
        try:
            events.append(json.loads(line.strip()))
        except Exception:
            continue

    if not events:
        st.info("No events to display.")
        return

    st.dataframe(events)

