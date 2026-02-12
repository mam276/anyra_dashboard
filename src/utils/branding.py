import streamlit as st
from pathlib import Path

def show_branding():
    # __file__ → points to: src/utils/branding.py
    # parent → src/utils
    # parent.parent → src/
    root = Path(__file__).parent.parent

    logo_path = root / "assets" / "anyra_logo.png"

    st.sidebar.image(str(logo_path), width=None)

