import json
import os

PENDING_FILE = "tickets/pending.json"

def add_pending(ticket):
    if not os.path.exists(PENDING_FILE):
        data = []
    else:
        with open(PENDING_FILE, "r") as f:
            data = json.load(f)

    data.append(ticket)

    with open(PENDING_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_pending():
    if not os.path.exists(PENDING_FILE):
        return []
    with open(PENDING_FILE, "r") as f:
        return json.load(f)


def remove_pending(index):
    data = get_pending()
    data.pop(index)
    with open(PENDING_FILE, "w") as f:
        json.dump(data, f, indent=2)
