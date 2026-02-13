# src/utils/email.py

import smtplib
from email.mime.text import MIMEText
import streamlit as st

def send_email(to: str, subject: str, body: str) -> bool:
    """
    Send an email using Office365 SMTP.
    Credentials are stored securely in st.secrets.
    """
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = st.secrets["SMTP_USER"]
        msg["To"] = to

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASSWORD"])
            server.sendmail(st.secrets["SMTP_USER"], [to], msg.as_string())

        print(f"[INFO] Email sent to {to}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email to {to}: {e}")
        return False
