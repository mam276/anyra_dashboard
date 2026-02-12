from utils.db import SessionLocal, ActivityLog

def log_action(user_id, action, details):
    db = SessionLocal()
    log = ActivityLog(user_id=user_id, action=action, details=details)
    db.add(log)
    db.commit()