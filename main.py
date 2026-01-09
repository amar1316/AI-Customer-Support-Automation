from core.intent_classifier import classify_intent
from knowledge_base.vector_store import fetch_knowledge
from core.response_generator import generate_response
from core.confidence_engine import calculate_confidence
from escalation.risk_rules import needs_escalation
from tickets.ticket_manager import log_ticket
from tickets.pending_store import add_pending
from datetime import datetime



message = input("Customer message: ")

intent = classify_intent(message)
knowledge = fetch_knowledge(intent)
response = generate_response(message, knowledge)
confidence = calculate_confidence(intent)

# inside escalation block
if needs_escalation(intent, confidence):
    action = "ESCALATED TO HUMAN"
    print("⚠️ Escalation required.")

    pending_ticket = {
        "timestamp": str(datetime.now()),
        "message": message,
        "intent": intent,
        "confidence": confidence,
        "suggested_reply": response
    }

    add_pending(pending_ticket)
else:
    action = "AUTO REPLIED"
    print("✅ AI Reply:")
    print(response)

log_ticket(message, intent, confidence, action)
