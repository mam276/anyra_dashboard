import streamlit as st
from utils.session import init_session
from utils.scheduler import start_scheduler
from utils.branding import show_branding

def main():
    init_session()
    start_scheduler()
    show_branding()

    menu = st.sidebar.radio("Navigation", [
        "Auth", "Data", "Analytics", "Visualization", "Insights",
        "Reports", "Payments", "Admin", "Inventory", "Copilot"
    ])

    if menu == "Auth":
        from modules.auth import views
        views.show_auth()
    elif menu == "Data":
        from modules.data_pipeline import services
        services.show_data_pipeline()
    elif menu == "Analytics":
        from modules.analytics import services
        services.show_analytics()
    elif menu == "Visualization":
        from modules.visualization import views
        views.show_visualization()
    elif menu == "Insights":
        from modules.insights import services
        services.show_insights()
    elif menu == "Reports":
        from modules.reporting import views
        views.show_reporting()
    elif menu == "Payments":
        from modules.payments import views
        views.show_payments()
    elif menu == "Admin":
        from modules.admin import views
        views.show_admin()
    elif menu == "Inventory":
        from modules.inventory import views
        views.show_inventory()
    elif menu == "Copilot":
        from modules.copilot import views
        views.show_copilot()

if __name__ == "__main__":
    main()