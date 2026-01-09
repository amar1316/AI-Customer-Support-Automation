def classify_intent(message: str) -> str:
    message = message.lower()

    if any(word in message for word in ["refund", "money back"]):
        return "refund"
    if any(word in message for word in ["bill", "payment", "invoice"]):
        return "billing"
    if any(word in message for word in ["error", "bug", "not working"]):
        return "technical_issue"
    if any(word in message for word in ["login", "password", "account"]):
        return "account_issue"
    if any(word in message for word in ["legal", "court", "sue"]):
        return "legal"
    
    return "general"
