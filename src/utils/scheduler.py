from apscheduler.schedulers.background import BackgroundScheduler
from anyra_dashboard.modules.utils.subscription import check_trials
from anyra_dashboard.modules.utils.file_manager import delete_expired_files

    scheduler = BackgroundScheduler()

def daily_report_generation():
    pass  # placeholder

def scheduled_cleanup(retention_days=30):
    delete_expired_files(retention_days=retention_days)

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(check_trials, "interval", hours=24)
        scheduler.add_job(daily_report_generation, "interval", hours=24)
        scheduler.add_job(scheduled_cleanup, "interval", hours=24)
        scheduler.start()






