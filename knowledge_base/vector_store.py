knowledge_base = {
    "refund": "Refunds are processed within 5–7 business days.",
    "billing": "Billing happens monthly. Invoice is sent to your email.",
    "technical_issue": "Please try restarting the application.",
    "account_issue": "Use the 'Forgot Password' option to reset.",
    "general": "Thank you for contacting support. We are happy to help."
}

def fetch_knowledge(intent: str) -> str:
    return knowledge_base.get(intent, knowledge_base["general"])
