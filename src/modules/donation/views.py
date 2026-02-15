import streamlit as st
import qrcode
from io import BytesIO
from utils.audit import log_event


# ---------------------------------------------------------
# QR Code Generator
# ---------------------------------------------------------
def generate_qr(data: str):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ---------------------------------------------------------
# Donation Screen
# ---------------------------------------------------------
def show_donation():
    st.title("Support ANYRA ❤️")
    st.write("Choose your preferred donation method below.")

    # -------------------------
    # Donation Amount
    # -------------------------
    amount = st.number_input("Donation Amount", min_value=1, step=1)
    upi_id = "nusratrabbilimited-2@okhdfcbank"
    name = "Mohammed Ashraf Moin"

    # -------------------------
    # Base UPI Link
    # -------------------------
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    # ---------------------------------------------------------
    # WORKING MOBILE UPI INTENT LINKS (Google Pay, PhonePe, Paytm)
    # ---------------------------------------------------------
    gpay_intent = (
        f"intent://upi/pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        "#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end;"
    )

    phonepe_intent = (
        f"intent://upi/pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        "#Intent;scheme=upi;package=com.phonepe.app;end;"
    )

    paytm_intent = (
        f"intent://upi/pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
        "#Intent;scheme=upi;package=net.one97.paytm;end;"
    )

    # ---------------------------------------------------------
    # Razorpay Global Payment Link
    # ---------------------------------------------------------
    razorpay_link = "https://rzp.io/l/ANYRA-Global-Donate"
    # Replace with your actual Razorpay payment link

    # ---------------------------------------------------------
    # PayPal Global Donation Link
    # ---------------------------------------------------------
    paypal_link = "https://www.paypal.com/donate/?hosted_button_id=YOUR_BUTTON_ID"
    # Replace with your PayPal donation button link

    # ---------------------------------------------------------
    # Mobile Tap-to-Pay Section
    # ---------------------------------------------------------
    st.subheader("Tap to Pay (Mobile Only)")
    st.write("If you're on a mobile device, tap one of the buttons below:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
        f"""
        <a href="javascript:window.location='{gpay_intent}';" 
           style="font-size:16px; font-weight:600;">
           Google Pay
        </a>
        """,
        unsafe_allow_html=True
        )

    with col2:
        st.markdown(
        f"""
        <a href="javascript:window.location='{phonepe_intent}';" 
           style="font-size:16px; font-weight:600;">
           PhonePe
        </a>
        """,
        unsafe_allow_html=True
        )

    with col3:
        st.markdown(
        f"""
        <a href="javascript:window.location='{paytm_intent}';" 
           style="font-size:16px; font-weight:600;">
           Paytm
        </a>
        """,
        unsafe_allow_html=True
        )

    st.divider()

    # ---------------------------------------------------------
    # Global Payment Options
    # ---------------------------------------------------------
    st.subheader("Global Donation Options 🌍")

    st.markdown(f"### 🌐 Donate via Razorpay (Global + India)\n[Click here to donate]({razorpay_link})")

    st.markdown(f"### 💳 Donate via PayPal (Global)\n[Donate with PayPal]({paypal_link})")

    st.divider()

    # ---------------------------------------------------------
    # QR Code for Desktop Users
    # ---------------------------------------------------------
    st.subheader("Scan to Pay (UPI – India Only)")
    qr_img = generate_qr(upi_link)
    st.image(qr_img, width=250)
    st.caption(f"UPI ID: **{upi_id}**")

    # ---------------------------------------------------------
    # Audit Logging
    # ---------------------------------------------------------
    user_email = st.session_state.get("user", {}).get("email", "guest")
    log_event(user_email, "donation_view", f"amount={amount}")

    st.success("Donation options generated successfully.")

