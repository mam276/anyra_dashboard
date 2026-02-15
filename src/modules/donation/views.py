import streamlit as st
import qrcode
from io import BytesIO
from utils.audit import log_event


def generate_qr(data: str):
    """Generate QR code image bytes."""
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def show_donation():
    st.title("Support ANYRA ❤️")

    st.write("Choose your preferred donation method below.")

    upi_id = "nusratrabbilimited-2@okhdfcbank"
    name = "Mohammed Ashraf Moin"
    amount = st.number_input("Donation Amount (INR)", min_value=1, step=1)

    # Base UPI link
    upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    # Mobile-friendly intent links
    gpay_link = (
        f"https://pay.google.com/gp/p/ui/pay?"
        f"pa={upi_id}&pn={name}&am={amount}&cu=INR"
    )

    phonepe_link = f"https://phon.pe/upi/{upi_id}?am={amount}&pn={name}"

    paytm_link = (
        f"paytmmp://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"
    )

    st.subheader("Tap to Pay (Mobile Only)")
    st.write("If you're on a mobile device, tap one of the buttons below:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[Google Pay]({gpay_link})")
    with col2:
        st.markdown(f"[PhonePe]({phonepe_link})")
    with col3:
        st.markdown(f"[Paytm]({paytm_link})")

    st.divider()

    st.subheader("Scan to Pay (Desktop & Mobile)")
    st.write("If you're on a laptop or desktop, scan this QR code:")

    qr_img = generate_qr(upi_link)
    st.image(qr_img, width=250)

    st.caption(f"UPI ID: **{upi_id}**")

    # Log donation intent
    user_email = st.session_state.get("user", {}).get("email", "guest")
    log_event(user_email, "donation_view", f"amount={amount}")

    st.success("Donation options generated successfully.")

