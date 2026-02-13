# src/utils/branding.py

from pathlib import Path
from PIL import Image
import streamlit as st

def show_branding():
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        try:
            img = Image.open(logo_path)
            img_width, _ = img.size

            sidebar_max_width = 280  # typical sidebar width

            # Always calculate a valid integer width
            if img_width > sidebar_max_width:
                scale_factor = sidebar_max_width / img_width
                display_width = int(img_width * scale_factor)
            else:
                display_width = int(img_width)

            # Debug log to confirm value
            print(f"[DEBUG] Logo width being used: {display_width}")

            # Pass only a valid integer width
            st.sidebar.image(str(logo_path), width=display_width)

        except Exception as e:
            # Fallback if image fails
            print(f"[ERROR] Branding image failed: {e}")
            st.sidebar.write("Anyra Dashboard")
    else:
        st.sidebar.write("Anyra Dashboard")

        st.sidebar.image(str(logo_path), width=display_width)
    else:
        st.sidebar.write("Anyra Dashboard")


