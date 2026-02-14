import os
import streamlit as st
from utils.session import init_session
from utils.scheduler import start_scheduler
from utils.branding import show_branding
from utils.rbac import enforce_role, enforce_subscription
from utils.tenants import get_tenant_data
from modules.auth import views as auth_views
from modules.onboarding import views as onboarding_views
from modules.donation import views as donation_views
from modules.audit import views as audit_views
from modules import crm

def show_logo():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        st.warning("Logo not found at expected path: " + logo_path)

def main():
    # Initialize session and scheduler
    init_session()
    start_scheduler()
    show_branding()

    # -------- Query Params Handling --------
    try:
        params = st.query_params
    except AttributeError:
        params = st.experimental_get_query_params()

    page = params.get("page", [None])[0]
    if page == "reset" and "token" in params:
        token = params["token"][0]
        auth_views.show_reset_form(token)
        return  # stop here after reset form

    # -------- Authentication Gate --------
    if st.session_state.get("user") is None:
        # Initialize welcome flag
        if "show_welcome" not in st.session_state:
            st.session_state["show_welcome"] = True

        if st.session_state["show_welcome"]:
            # Show welcome screen first
            
            show_logo()

            st.title("Welcome to Anyra Dashboard 👋")
            st.write("Explore insights tailored to your data — sign up or log in to continue.")

            if st.button("Continue"):
                st.session_state["show_welcome"] = False
            return  # stop here after welcome screen

        # Unified login/signup screen (tabs)
        auth_views.show_auth()
        return  # stop here until user logs in

    # -------- Onboarding Flows (only after login) --------
    onboarding_views.show_welcome_popup()
    onboarding_views.show_rotating_tips()
    onboarding_views.start_guided_tour()

    # -------- Sidebar Navigation --------
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Navigation",
        [
            "Auth", "Data", "Analytics", "Visualization", "Insights",
            "Reports", "Payments", "Admin", "Inventory", "Copilot", "CRM",
            "Donation", "Audit"
        ]
    )

    if menu == "Auth":
        auth_choice = st.sidebar.radio("Auth Options", ["Login/Signup", "Forgot Password"])
        if auth_choice == "Login/Signup":
            auth_views.show_auth()
        elif auth_choice == "Forgot Password":
            auth_views.show_forgot_password()

    elif menu == "Data":
        from modules.data_pipeline import services
        services.show_data_pipeline()

    elif menu == "Analytics":
        from modules.analytics import services
        if enforce_subscription("premium"):
            services.show_analytics()
        else:
            st.error("Upgrade to premium to access Analytics.")

    elif menu == "Visualization":
        from modules.visualization import views
        views.show_visualization()

    elif menu == "Insights":
        from modules.insights import services
        services.show_insights()

    elif menu == "Reports":
        from modules.reporting import views
        if enforce_subscription("premium"):
            views.show_reporting()
        else:
            st.error("Upgrade to premium to access Reports.")

    elif menu == "Payments":
        from modules.payments import views
        if enforce_role("admin"):
            views.show_payments()
        else:
            st.error("You do not have permission to access Payments management.")

    elif menu == "Admin":
        from modules.admin import views
        if enforce_role("admin"):
            views.show_admin()
        else:
            st.error("You do not have permission to access Admin dashboard.")

    elif menu == "Inventory":
        from modules.inventory import views
        views.show_inventory()

    elif menu == "Copilot":
        from modules.copilot import views
        views.show_copilot()

    elif menu == "CRM":
        from modules.crm import views
        if enforce_subscription("premium") or enforce_role("admin"):
            views.show_crm_dashboard()
        else:
            st.error("CRM is available only to premium users or admin role.")

    elif menu == "Donation":
        if st.session_state.get("user"):
            donation_views.show_donation()
        else:
            st.error("You must be logged in to access donations.")

    elif menu == "Audit":
        if enforce_role("admin"):
            audit_views.show_audit_dashboard()
        else:
            st.error("You do not have permission to view audit logs.")


if __name__ == "__main__":
    main()

