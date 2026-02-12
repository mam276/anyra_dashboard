import datetime
from utils.db import SessionLocal, Subscription

def check_trials():
    db = SessionLocal()
    subs = db.query(Subscription).filter(Subscription.plan=="trial", Subscription.active==True).all()
    now = datetime.datetime.utcnow()
    for sub in subs:
        if sub.trial_end_date and sub.trial_end_date < now:
            sub.active = False
            db.commit()