import qrcode
import os

def generate_upi_qr(user_id, upi_id="your-upi-id@bank", amount=0):
    upi_url = f"upi://pay?pa={upi_id}&pn=AnyraDashboard&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)

    folder = f"data_storage/user_{user_id}/payments"
    os.makedirs(folder, exist_ok=True)
    filepath = f"{folder}/upi_qr.png"
    qr.save(filepath)

    return filepath