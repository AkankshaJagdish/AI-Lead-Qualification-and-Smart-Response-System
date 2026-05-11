import re

from .models import LeadInput


PERSONAL_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "aol.com",
    "icloud.com",
}


def sanitize_lead(lead: LeadInput) -> LeadInput:
    """Normalize textual fields to reduce noisy user input."""
    cleaned_message = re.sub(r"\s+", " ", lead.message).strip()
    return lead.model_copy(
        update={
            "full_name": lead.full_name.strip(),
            "company": lead.company.strip(),
            "message": cleaned_message,
            "email": lead.email.lower(),
        }
    )


def is_company_email(email: str) -> bool:
    domain = email.split("@")[-1].lower()
    return domain not in PERSONAL_EMAIL_DOMAINS
