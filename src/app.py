import streamlit as st
from utils.session import init_session
from utils.scheduler import start_scheduler
from utils.branding import show_branding
from utils.rbac import enforce_role, enforce_subscription
from utils.tenants import get_tenant_data
from modules.auth import views as auth_views


def main():
    # Run login/authentication first
    auth_views.login_user()
    init_session()
    show_branding()

    # Sidebar navigation
    menu = st.sidebar.radio(
        "Navigation",
        [
            "Auth", "Data", "Analytics", "Visualization", "Insights",
            "Reports", "Payments", "Admin", "Inventory", "Copilot"
        ]
    )

    if menu == "Auth":
        from modules.auth import views
        views.show_auth()

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

if __name__ == "__main__":
    main()


















