def needs_escalation(intent: str, confidence: int) -> bool:
    if intent in ["legal"]:
        return True
    if confidence < 60:
        return True
    return False
