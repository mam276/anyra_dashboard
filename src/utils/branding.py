from pathlib import Path
from PIL import Image
import streamlit as st

def show_branding():
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        # Load image to inspect its dimensions
        img = Image.open(logo_path)
        img_width, img_height = img.size

        # Streamlit sidebar is roughly 300px wide by default
        sidebar_max_width = 280  

        # Scale proportionally if image is wider than sidebar
        if img_width > sidebar_max_width:
            scale_factor = sidebar_max_width / img_width
            display_width = int(img_width * scale_factor)
        else:
            display_width = img_width  # keep original size if smaller

        st.sidebar.image(str(logo_path), width=display_width)
    else:
        st.sidebar.write("Anyra Dashboard")
