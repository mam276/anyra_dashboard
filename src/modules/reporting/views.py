import streamlit as st
from fpdf import FPDF
import os

def show_reporting():
    st.subheader("Reporting")
    df = st.session_state.get("data")
    user = st.session_state.get("user")
    if df is None or not user:
        st.warning("Upload data first.")
        return

    if st.button("Generate PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Anyra Dashboard Report", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Author: ASHRAF", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Rows: {df.shape[0]}, Columns: {df.shape[1]}", ln=True)
        folder = f"data_storage/user_{user['id']}/reports"
        os.makedirs(folder, exist_ok=True)
        filepath = f"{folder}/report.pdf"
        pdf.output(filepath)
        st.success(f"Report saved to {filepath}")