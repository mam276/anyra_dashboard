# src/utils/audit.py

import datetime
import json
import os

LOG_FILE = os.getenv("AUDIT_LOG_FILE", "audit.log")

def log_action(user: str, action: str) -> bool:
    """
    Log user/admin actions for audit purposes.
    Writes to a JSON-formatted text file; replace with DB or logging service in production.
    Returns True if log entry was written successfully.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user,
        "action": action
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[AUDIT] {entry}")  # optional console output
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write audit log: {e}")
        return False
