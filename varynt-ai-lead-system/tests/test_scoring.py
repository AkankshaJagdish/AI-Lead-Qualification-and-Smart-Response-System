from app.classifier import classify
from app.models import LeadInput
from app.scoring import score_lead


def test_hot_lead_scoring():
    lead = LeadInput(
        full_name="Jane Doe",
        email="jane@enterprise.com",
        company="Acme",
        budget_usd=120000,
        urgency="high",
        message="We want to buy now and need a proposal, pricing, and implementation timeline this month.",
    )
    result = score_lead(lead)
    assert result.lead_score >= 70
    assert classify(result.lead_score) == "HOT"


def test_cold_lead_scoring():
    lead = LeadInput(
        full_name="John",
        email="john@gmail.com",
        company="Solo",
        budget_usd=1000,
        urgency="low",
        message="Curious to learn more.",
    )
    result = score_lead(lead)
    assert result.lead_score < 40
    assert classify(result.lead_score) == "COLD"
