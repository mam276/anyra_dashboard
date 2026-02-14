import streamlit as st
import pandas as pd
from utils.session import current_user
from utils.db import SessionLocal, ActivityLog
from modules.insights.services import insights_coverage

def show_copilot():
    st.subheader("Copilot Assistant")
    user = current_user()
    df = st.session_state.get("data")

    if not user:
        st.warning("Please login first.")
        return

    st.info(f"Hello {user['email']}! I’m your Copilot guide.")

    if df is not None:
        coverage = insights_coverage(df)
        available = [c for c in coverage if c["available"] == "✔ Available"]
        missing = [c for c in coverage if c["available"] == "✘ Missing"]

        st.success(f"{len(available)} insights available.")
        if missing:
            st.info("Some insights are missing. To unlock them, add columns:")
            for m in missing:
                st.write(f"- {m['metric']} requires {m['required_cols']}")

        st.download_button(
            "Download Coverage Report (CSV)",
            data=pd.DataFrame(coverage).to_csv(index=False),
            file_name="coverage_report.csv",
            mime="text/csv"
        )

    # Show last activity
    db = SessionLocal()
    last_log = db.query(ActivityLog).filter(ActivityLog.user_id == user["id"]).order_by(ActivityLog.timestamp.desc()).first()
    db.close()
    if last_log:
        st.write("Last Activity:", f"{last_log.action} - {last_log.details}")
