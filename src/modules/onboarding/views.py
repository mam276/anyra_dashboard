# src/modules/onboarding/views.py

import streamlit as st
import time
import random

def show_welcome_popup():
    """
    Show a short welcome popup for new/unregistered users.
    Appears for 5 seconds or disappears on click.
    """
    role = st.session_state.get("role", "guest")
    subscription = st.session_state.get("subscription_level", "free")

    # Only show for guest/free/trial users, not admin/premium
    if role not in ["admin"] and subscription in ["free", "trial"]:
        if "popup_shown" not in st.session_state:
            st.session_state["popup_shown"] = True
            popup = st.empty()

            # Choose message dynamically
            if role == "guest":
                message = "👋 Welcome! Explore insights tailored to your data — sign up today to unlock your dashboard."
            elif subscription == "free":
                message = "You’re on the free plan — enjoy core analytics. Upgrade anytime for premium features."
            elif subscription == "trial":
                message = "Your trial unlocks premium features — explore advanced analytics before it ends!"
            else:
                message = "Welcome to the dashboard!"

            with popup.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f8ff;
                        padding:20px;
                        border-radius:10px;
                        text-align:center;
                        font-size:16px;
                        cursor:pointer;">
                        {message}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # Auto-hide after 5 seconds
            time.sleep(5)
            popup.empty()


def show_rotating_tips():
    """
    Show rotating 'Did you know?' tips for free users.
    Each session displays one random tip.
    """
    tips = [
        "📊 Did you know? You can upload CSV files and instantly visualize your data.",
        "🔍 Did you know? Premium users unlock advanced analytics and executive dashboards.",
        "📈 Did you know? You can generate automated reports with one click.",
        "🛡️ Did you know? Multi-tenant isolation keeps your data secure and private.",
        "🤖 Did you know? Copilot can guide you through deeper insights based on your data columns."
    ]

    role = st.session_state.get("role", "guest")
    subscription = st.session_state.get("subscription_level", "free")

    if role not in ["admin"] and subscription == "free":
        if "tip_shown" not in st.session_state:
            st.session_state["tip_shown"] = True
            tip = random.choice(tips)
            st.info(tip)

def start_guided_tour():
    """
    Step-by-step guided tour for new users.
    """
    role = st.session_state.get("role", "guest")
    subscription = st.session_state.get("subscription_level", "free")

    # Only show for guest/free users
    if role in ["admin", "premium"]:
        return

    if "tour_completed" in st.session_state:
        return

    if "tour_step" not in st.session_state:
        st.session_state["tour_step"] = 0

    steps = [
        "📂 Use the sidebar to navigate between modules like Analytics, CRM, and Payments.",
        "📤 Upload your CSV or Excel files to start exploring your data.",
        "📊 Generate charts and dashboards instantly from your uploaded data.",
        "📑 Export insights and share reports with your team.",
        "🚀 Upgrade to premium for executive dashboards, predictive analytics, and advanced features."
    ]

    step = st.session_state["tour_step"]

    st.markdown(
        f"""
        <div style="
            background-color:#e6f7ff;
            padding:20px;
            border-radius:10px;
            font-size:16px;">
            {steps[step]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Next"):
            if step + 1 < len(steps):
                st.session_state["tour_step"] += 1
            else:
                st.session_state["tour_completed"] = True
                st.session_state.pop("tour_step")
    with col2:
        if st.button("Skip Tour"):
            st.session_state["tour_completed"] = True
            st.session_state.pop("tour_step")
