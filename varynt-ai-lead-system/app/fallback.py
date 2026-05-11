from .models import AIResponse, LeadInput


def fallback_response(lead: LeadInput, classification: str) -> AIResponse:
    """Safe deterministic fallback when AI call times out/fails."""
    subject = f"Thanks for contacting VARYNT ({classification} lead)"
    body = (
        f"Hi {lead.full_name}, thanks for reaching out to VARYNT. "
        f"We received your request and our team will follow up shortly with next steps "
        f"tailored to your goals at {lead.company}."
    )
    return AIResponse(subject=subject, message=body)
