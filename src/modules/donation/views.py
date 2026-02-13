import streamlit as st
from utils.audit import log_event

def show_donation():
    """
    Donation module for Anyra Dashboard.
    Supports multiple payment methods (Stripe, PayPal, UPI).
    """
    st.subheader("Support Anyra Dashboard ❤️")
    st.write("Your contributions help us improve and keep the service running.")

    # Payment links (replace with real ones)
    stripe_url = "https://checkout.stripe.com/pay/cs_test_12345"
    paypal_url = "https://www.paypal.com/donate/?hosted_button_id=YOUR_BUTTON_ID"
    upi_url = "upi://pay?pa=yourupi@bank&pn=AnyraDashboard&cu=INR"

    user = st.session_state.get("user", "anonymous")

    if st.button("Donate via Stripe"):
        log_event(user, "donation_attempt", "Stripe")
        st.markdown(f"[Click here to complete donation]({stripe_url})")

    if st.button("Donate via PayPal"):
        log_event(user, "donation_attempt", "PayPal")
        st.markdown(f"[Click here to complete donation]({paypal_url})")

    if st.button("Donate via UPI"):
        log_event(user, "donation_attempt", "UPI")
        st.markdown(f"[Click here to complete donation]({upi_url})")



