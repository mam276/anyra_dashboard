import smtplib
from email.mime.text import MIMEText
import streamlit as st

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = st.secrets["SMTP_USER"]
    msg["To"] = to

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(st.secrets["SMTP_USER"], st.secrets["SMTP_PASSWORD"])
        server.sendmail(st.secrets["SMTP_USER"], [to], msg.as_string())