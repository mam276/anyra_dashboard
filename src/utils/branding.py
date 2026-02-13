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
            sidebar_max_width = 280

            if img_width > sidebar_max_width:
                scale_factor = sidebar_max_width / img_width
                display_width = int(img_width * scale_factor)
                st.sidebar.image(str(logo_path), width=display_width)
            else:
                st.sidebar.image(str(logo_path))
        except Exception as e:
            print(f"[ERROR] Branding image failed: {e}")
            st.sidebar.write("Anyra Dashboard")
    else:
        st.sidebar.write("Anyra Dashboard")

        except Exception as e:
            print(f"[ERROR] Branding image failed: {e}")
            st.sidebar.write("Anyra Dashboard")
    else:
        st.sidebar.write("Anyra Dashboard")

