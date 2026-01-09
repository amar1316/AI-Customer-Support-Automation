from core.llm_client import call_llm
from core.prompts import support_prompt

def generate_response(customer_message: str, knowledge: str) -> str:
    prompt = support_prompt(customer_message, knowledge)
    return call_llm(prompt)
