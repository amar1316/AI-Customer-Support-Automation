def calculate_confidence(intent: str) -> int:
    high_confidence = ["billing", "general", "account_issue"]
    medium_confidence = ["technical_issue"]
    low_confidence = ["refund", "legal"]

    if intent in high_confidence:
        return 90
    if intent in medium_confidence:
        return 70
    return 40