from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
import json

# -------------------------------
# CORE IMPORTS
# -------------------------------
from core.intent_classifier import classify_intent
from knowledge_base.vector_store import fetch_knowledge
from core.response_generator import generate_response
from core.confidence_engine import calculate_confidence
from escalation.risk_rules import needs_escalation
from tickets.ticket_manager import log_ticket
from tickets.pending_store import add_pending, get_pending, remove_pending

# -------------------------------
# FASTAPI APP
# -------------------------------
app = FastAPI(title="AI Customer Support API")

# Ensure folders exist (VERY IMPORTANT for Render)
os.makedirs("logs", exist_ok=True)
os.makedirs("tickets", exist_ok=True)

# -------------------------------
# MODELS
# -------------------------------
class SupportRequest(BaseModel):
    message: str


class SupportResponse(BaseModel):
    intent: str
    confidence: int
    action: str
    reply: Optional[str] = None


# -------------------------------
# MAIN SUPPORT ENDPOINT
# -------------------------------
@app.post("/support", response_model=SupportResponse)
def handle_support(req: SupportRequest):
    message = req.message

    intent = classify_intent(message)
    knowledge = fetch_knowledge(intent)
    reply = generate_response(message, knowledge)
    confidence = calculate_confidence(intent)

    # Escalation path
    if needs_escalation(intent, confidence):
        action = "ESCALATED_TO_HUMAN"

        add_pending({
            "timestamp": str(datetime.now()),
            "message": message,
            "intent": intent,
            "confidence": confidence,
            "suggested_reply": reply
        })

        log_ticket(message, intent, confidence, action)

        return {
            "intent": intent,
            "confidence": confidence,
            "action": action,
            "reply": None
        }

    # Auto-reply path
    action = "AUTO_REPLIED"
    log_ticket(message, intent, confidence, action)

    return {
        "intent": intent,
        "confidence": confidence,
        "action": action,
        "reply": reply
    }


# -------------------------------
# PENDING TICKETS
# -------------------------------
@app.get("/pending")
def fetch_pending_tickets():
    return get_pending()


@app.post("/approve/{index}")
def approve_ticket(index: int, payload: dict | None = None):
    pending = get_pending()

    if index >= len(pending):
        return {"status": "invalid index"}

    ticket = pending[index]

    final_reply = None
    if payload:
        final_reply = payload.get("final_reply")

    log_ticket(
        ticket["message"],
        ticket["intent"],
        ticket["confidence"],
        "HUMAN_APPROVED"
    )

    remove_pending(index)

    return {
        "status": "approved",
        "final_reply": final_reply
    }



@app.post("/reject/{index}")
def reject_ticket(index: int):
    pending = get_pending()

    if index >= len(pending):
        return {"status": "invalid index"}

    ticket = pending[index]

    log_ticket(
        ticket["message"],
        ticket["intent"],
        ticket["confidence"],
        "HUMAN_REJECTED"
    )

    remove_pending(index)
    return {"status": "rejected"}



# -------------------------------
# AUDIT LOGS (SQLite-LINES SAFE)
# -------------------------------
@app.get("/logs")
def get_audit_logs():
    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute("""
        SELECT timestamp, message, intent, confidence, action
        FROM audit_logs
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


