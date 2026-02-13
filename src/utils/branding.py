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

            if img_width > sidebar_max_width:
                # Scale proportionally and force integer
                scale_factor = sidebar_max_width / img_width
                display_width = int(img_width * scale_factor)

                # Debug log to confirm
                print(f"[DEBUG] Scaled logo width: {display_width}")

                st.sidebar.image(str(logo_path), width=display_width)
            else:
                # Let Streamlit auto-scale (no width argument)
                print(f"[DEBUG] Using natural logo width: {img_width}")
                st.sidebar.image(str(logo_path))

        except Exception as e:
            print(f"[ERROR] Branding image failed: {e}")
            st.sidebar.write("Anyra Dashboard")
    else:
        st.sidebar.write("Anyra Dashboard")
