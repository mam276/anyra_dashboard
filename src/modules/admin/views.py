import streamlit as st
from utils.file_manager import delete_expired_files
from utils.db import SessionLocal, ActivityLog

def show_admin():
    st.subheader("Admin Dashboard")
    retention_days = st.number_input("Retention period (days)",1,3650,30)
    if st.button("Apply Retention Policy"):
        delete_expired_files(retention_days=retention_days)
        st.success(f"Files older than {retention_days} days deleted.")

    st.subheader("File Deletion Logs")
    db = SessionLocal()
    logs = db.query(ActivityLog).filter(ActivityLog.action.in_(["file_deleted","folder_deleted"])).order_by(ActivityLog.timestamp.desc()).limit(20).all()
    for log in logs:
        st.write(f"[{log.timestamp}] User {log.user_id} - {log.action}: {log.details}")