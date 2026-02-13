import streamlit as st
import json
import os

LOG_FILE = "logs/audit.log"

def show_audit_dashboard():
    """
    Admin dashboard for viewing audit logs in real time.
    Displays authentication, RBAC, onboarding, and donation events.
    """
    st.subheader("Audit Dashboard 📜")
    st.write("Monitor system events, user actions, and donations in real time.")

    if not os.path.exists(LOG_FILE):
        st.warning("No audit logs found yet.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    events = []
    for line in lines[-200:]:  # show last 200 events
        try:
            events.append(json.loads(line.strip()))
        except Exception:
            continue

    if not events:
        st.info("No events to display.")
        return

    # Show raw events
    st.markdown("### Recent Events")
    st.dataframe(events)

    # Filter by event type
    event_types = sorted(set(e.get("event") for e in events if "event" in e))
    selected = st.selectbox("Filter by event type", ["All"] + event_types)

    if selected != "All":
        filtered = [e for e in events if e.get("event") == selected]
        st.dataframe(filtered)

    # Summary counts
    st.markdown("### Event Summary")
    summary = {etype: sum(1 for e in events if e.get("event") == etype) for etype in event_types}
    st.json(summary)

    # Quick stats widgets
    st.markdown("### Quick Stats")
    cols = st.columns(len(summary))
    for i, (etype, count) in enumerate(summary.items()):
        cols[i].metric(label=etype, value=count)
