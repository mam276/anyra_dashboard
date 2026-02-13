from pathlib import Path
from PIL import Image
import streamlit as st

def show_branding():
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        img = Image.open(logo_path)
        img_width, _ = img.size

        sidebar_max_width = 280  # typical sidebar width

        if img_width > sidebar_max_width:
            scale_factor = sidebar_max_width / img_width
            display_width = int(img_width * scale_factor)  # ensure integer
        else:
            display_width = int(img_width)  # force integer
#--------------DEBUG LINE --------
        st.write(f"Logo width being used: {display_width}")
#---------------------------------
        st.sidebar.image(str(logo_path), width=display_width)
    else:
        st.sidebar.write("Anyra Dashboard")

        st.sidebar.image(str(logo_path), width=display_width)
    else:
        st.sidebar.write("Anyra Dashboard")

