import json
import logging
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI

from .ai_client import AIClient
from .classifier import classify
from .models import LeadInput, LeadOutput
from .responder import generate_response
from .scoring import score_lead
from .validators import sanitize_lead

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("varynt.api")

app = FastAPI(title="VARYNT AI Lead Qualification System", version="0.1.0")

conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS lead_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        email TEXT NOT NULL,
        classification TEXT NOT NULL,
        lead_score INTEGER NOT NULL,
        payload_json TEXT NOT NULL
    )
    """
)
conn.commit()


@app.post("/leads/qualify", response_model=LeadOutput)
def qualify_lead(lead: LeadInput) -> LeadOutput:
    clean = sanitize_lead(lead)
    scoring_result = score_lead(clean)
    classification = classify(scoring_result.lead_score)

    ai_response = generate_response(clean, classification, scoring_result.lead_score, AIClient())

    output = LeadOutput(
        lead_score=scoring_result.lead_score,
        classification=classification,
        response=ai_response,
    )

    conn.execute(
        "INSERT INTO lead_events (created_at, email, classification, lead_score, payload_json) VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(),
            clean.email,
            classification,
            scoring_result.lead_score,
            json.dumps(output.model_dump()),
        ),
    )
    conn.commit()

    logger.info("lead_qualified", extra={"email": clean.email, "classification": classification, "score": scoring_result.lead_score})
    return output
