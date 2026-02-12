from apscheduler.schedulers.background import BackgroundScheduler
from utils.subscription import check_trials
from utils.file_manager import delete_expired_files

# Global scheduler instance (singleton)
scheduler = None

def daily_report_generation():
    pass

def scheduled_cleanup(retention_days=30):
    delete_expired_files(retention_days=retention_days)

def start_scheduler():
    global scheduler

    # Create scheduler only once globally
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(check_trials, "interval", hours=24)
        scheduler.add_job(daily_report_generation, "interval", hours=24)
        scheduler.add_job(scheduled_cleanup, "interval", hours=24)
        scheduler.start()



