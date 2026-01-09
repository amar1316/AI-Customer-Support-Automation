import json
import os
from datetime import datetime

LOG_FILE = "logs/audit_log.json"

def log_ticket(message, intent, confidence, action):
    log = {
        "timestamp": str(datetime.now()),
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "action": action
    }

    # Load existing logs
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    # Append new log
    data.append(log)

    # Save back as proper JSON
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
