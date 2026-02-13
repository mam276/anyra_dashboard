# src/utils/audit.py

import datetime

def log_action(user: str, action: str):
    """
    Log admin actions for audit purposes.
    Writes to a simple text file; replace with DB or logging service in production.
    """
    timestamp = datetime.datetime.now().isoformat()
    with open("audit.log", "a") as f:
        f.write(f"{timestamp} | {user} | {action}\n")
