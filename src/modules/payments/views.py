import streamlit as st
from utils.upi import generate_upi_qr

def show_payments():
    st.subheader("Payments & Subscription")
    user = st.session_state.get("user")
    if not user:
        st.warning("Please login first.")
        return

    st.write("Choose your payment method:")
    method = st.radio("Payment Method", ["UPI", "PayPal", "Card"])

    if method == "UPI":
        upi_id = st.text_input("Enter UPI ID", "your-upi-id@bank")
        amount = st.number_input("Amount (INR)", min_value=0.0, step=100.0)
        if st.button("Generate UPI QR"):
            filepath = generate_upi_qr(user["id"], upi_id, amount)
            st.image(filepath, caption="Scan this QR to pay via UPI")
            st.success("UPI QR code generated successfully.")

    elif method == "PayPal":
        st.info("PayPal integration placeholder — requires API keys in secrets.")
    elif method == "Card":
        st.info("Card payment integration placeholder — requires Stripe API keys.")