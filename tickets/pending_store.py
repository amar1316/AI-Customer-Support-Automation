import json
import os

PENDING_DIR = "tickets"
PENDING_FILE = os.path.join(PENDING_DIR, "pending.json")

def get_pending():
    if not os.path.exists(PENDING_FILE):
        return []
    with open(PENDING_FILE, "r") as f:
        return json.load(f)

def add_pending(ticket):
    os.makedirs(PENDING_DIR, exist_ok=True)
    data = get_pending()
    data.append(ticket)
    with open(PENDING_FILE, "w") as f:
        json.dump(data, f, indent=2)

def remove_pending(index):
    data = get_pending()
    if index < len(data):
        data.pop(index)
        with open(PENDING_FILE, "w") as f:
            json.dump(data, f, indent=2)
