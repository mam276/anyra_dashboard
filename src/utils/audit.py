import datetime
import json
import os

LOG_FILE = os.getenv("AUDIT_LOG_FILE", "logs/audit.log")

def log_event(user: str, event: str, details: str = "") -> bool:
    """
    Unified audit logger for Anyra Dashboard.
    Records authentication, RBAC, onboarding, and donation events.
    Writes JSON lines to a text file.
    """
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user or "anonymous",
        "event": event,
        "details": details
    }

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[AUDIT] {entry}")  # optional console output
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write audit log: {e}")
        return False
