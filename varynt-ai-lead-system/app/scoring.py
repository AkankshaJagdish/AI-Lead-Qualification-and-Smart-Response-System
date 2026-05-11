from .models import LeadInput, LeadScoringResult
from .validators import is_company_email

INTENT_KEYWORDS = {
    "buy",
    "purchase",
    "proposal",
    "demo",
    "timeline",
    "contract",
    "pricing",
    "implementation",
}


def _budget_score(budget_usd: float | None) -> int:
    if budget_usd is None:
        return 0
    if budget_usd >= 100000:
        return 30
    if budget_usd >= 50000:
        return 22
    if budget_usd >= 20000:
        return 15
    if budget_usd >= 5000:
        return 8
    return 3


def _urgency_score(urgency: str) -> int:
    return {"high": 25, "medium": 12, "low": 5}.get(urgency, 0)


def _intent_score(message: str) -> int:
    text = message.lower()
    hits = sum(1 for kw in INTENT_KEYWORDS if kw in text)
    return min(hits * 8, 24)


def _message_completeness(message: str) -> int:
    words = len(message.split())
    if words >= 80:
        return 15
    if words >= 40:
        return 10
    if words >= 20:
        return 6
    return 2


def score_lead(lead: LeadInput) -> LeadScoringResult:
    """Deterministic score to keep qualification transparent and testable."""
    score = 0
    score += _budget_score(lead.budget_usd)
    score += _urgency_score(lead.urgency.value)
    score += _intent_score(lead.message)
    score += _message_completeness(lead.message)
    score += 6 if is_company_email(lead.email) else 0

    score = max(0, min(score, 100))
    return LeadScoringResult(lead_score=score, classification="")
