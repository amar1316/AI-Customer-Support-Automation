import json
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "audit_log.json")

def log_ticket(message, intent, confidence, action):
    os.makedirs(LOG_DIR, exist_ok=True)

    log = {
        "timestamp": str(datetime.now()),
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "action": action
    }

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        except:
            data = []
    else:
        data = []

    data.append(log)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
