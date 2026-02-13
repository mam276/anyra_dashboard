import streamlit as st
from utils.session import init_session
from utils.scheduler import start_scheduler
from utils.branding import show_branding
from utils.rbac import enforce_role, enforce_subscription
from utils.tenants import get_tenant_data
from modules.auth import views as auth_views
from modules.onboarding import views as onboarding_views
from modules import crm

def main():
    # Initialize session and scheduler
    init_session()
    start_scheduler()
    show_branding()

    # Show Welcome popup
    onboarding_views.show_welcome_popup()

    # Show rotating tip for free users
    onboarding_views.show_rotating_tips()

    # Start guided tour for new users
    onboarding_views.start_guided_tour()
   
    # Check query params for reset route
    try:
        params = st.query_params
    except AttributeError:
        params = st.experimental_get_query_params()

    if params.get("page") == ["reset"] and "token" in params:
        token = params["token"][0]
        auth_views.show_reset_form(token)
        return
        
    #--------Authentication Gate -----------------
    if st.session_state.get("user") is None:
        # Show welcome screen first
        st.title("Welcome to Anyra Dashboard 👋")
        st.write("Please sign up or log in to continue.")

        # Only then show login/signup form
        auth_views.login_user()
        return  # stop here until user logs in

    # Sidebar navigation
    menu = st.sidebar.radio(
        "Navigation",
        [
            "Auth", "Data", "Analytics", "Visualization", "Insights",
            "Reports", "Payments", "Admin", "Inventory", "Copilot", "CRM"
        ]
    )

    if menu == "Auth":
        from modules.auth import views
        auth_choice = st.sidebar.radio("Auth Options", ["Login/Signup", "Forgot Password"])
        if auth_choice == "Login/Signup":
            views.show_auth()
        elif auth_choice == "Forgot Password":
            views.show_forgot_password()

    elif menu == "Data":
        from modules.data_pipeline import services
        services.show_data_pipeline()

    elif menu == "Analytics":
        from modules.analytics import services
        # Subscription enforcement
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
        # Subscription enforcement
        if enforce_subscription("premium"):
            views.show_reporting()
        else:
            st.error("Upgrade to premium to access Reports.")

    elif menu == "Payments":
        from modules.payments import views
        # Admin only
        if enforce_role("admin"):
            views.show_payments()
        else:
            st.error("You do not have permission to access Payments management.")

    elif menu == "Admin":
        from modules.admin import views
        # Admin only
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
        # Only allow premium subscribers or admin role
        if enforce_subscription("premium") or enforce_role("admin"):
            views.show_crm_dashboard()
        else:
            st.error("CRM is available only to premium users or admin role.")

if __name__ == "__main__":
    main()









