from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

from core.intent_classifier import classify_intent
from knowledge_base.vector_store import fetch_knowledge
from core.response_generator import generate_response
from core.confidence_engine import calculate_confidence
from escalation.risk_rules import needs_escalation
from tickets.ticket_manager import log_ticket
from tickets.pending_store import add_pending

# 🚨 THIS LINE IS REQUIRED BY UVICORN
app = FastAPI(title="AI Customer Support API")


class SupportRequest(BaseModel):
    message: str


class SupportResponse(BaseModel):
    intent: str
    confidence: int
    action: str
    reply: str | None = None


@app.post("/support", response_model=SupportResponse)
def handle_support(req: SupportRequest):

    message = req.message

    intent = classify_intent(message)
    knowledge = fetch_knowledge(intent)
    reply = generate_response(message, knowledge)
    confidence = calculate_confidence(intent)


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

    else:
        action = "AUTO_REPLIED"
        log_ticket(message, intent, confidence, action)

        return {
            "intent": intent,
            "confidence": confidence,
            "action": action,
            "reply": reply
        }
