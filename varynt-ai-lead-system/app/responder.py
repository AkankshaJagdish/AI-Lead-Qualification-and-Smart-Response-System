from .ai_client import AIClient
from .fallback import fallback_response
from .models import AIResponse, LeadInput


def build_prompt(lead: LeadInput, classification: str, score: int) -> str:
    return (
        f"Create an email reply for a {classification} lead (score: {score}). "
        f"Lead: {lead.full_name} from {lead.company}, budget: {lead.budget_usd}, urgency: {lead.urgency.value}. "
        f"Original message: {lead.message}. "
        "Return exactly two lines in this format:\n"
        "Subject: ...\n"
        "Message: ..."
    )


def generate_response(lead: LeadInput, classification: str, score: int, ai_client: AIClient) -> AIResponse:
    prompt = build_prompt(lead, classification, score)
    try:
        raw = ai_client.generate_reply(prompt)
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        subject = next((l.replace("Subject:", "").strip() for l in lines if l.lower().startswith("subject:")), "")
        message = next((l.replace("Message:", "").strip() for l in lines if l.lower().startswith("message:")), "")
        if not subject or not message:
            raise ValueError("invalid AI format")
        return AIResponse(subject=subject[:140], message=message[:900])
    except Exception:
        return fallback_response(lead, classification)
