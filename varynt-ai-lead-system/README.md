# VARYNT AI Lead Qualification + Smart Response System

A lightweight, production-aware MVP for qualifying inbound leads with deterministic rules and AI-personalized follow-up.

## Why this architecture

This project intentionally separates core lead qualification (deterministic and testable) from AI personalization (probabilistic and failure-prone):

- **Scoring engine (`scoring.py`)**: rule-based, transparent, easy to tune.
- **Classifier (`classifier.py`)**: simple threshold mapping (`HOT/WARM/COLD`).
- **Responder (`responder.py`)**: AI used only for crafting response tone/content.
- **Fallback (`fallback.py`)**: deterministic backup response when AI fails.
- **API (`main.py`)**: request validation, orchestration, basic persistence, logging.

This keeps reliability high while still using AI where it adds value.

## Features

- FastAPI endpoint: `POST /leads/qualify`
- Pydantic validation + sanitization
- Deterministic lead score (0–100)
- Classification: `HOT >= 70`, `WARM >= 40`, else `COLD`
- OpenAI-based personalized response generation
- Fallback responses on timeout/API failures
- Retry and timeout support for AI calls
- Structured logging-friendly events
- In-memory SQLite event persistence for lightweight audit trail
- pytest unit + API tests

## Project layout

```
varynt-ai-lead-system/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── scoring.py
│   ├── classifier.py
│   ├── responder.py
│   ├── ai_client.py
│   ├── validators.py
│   ├── fallback.py
│   └── config.py
├── tests/
│   ├── test_scoring.py
│   └── test_api.py
├── README.md
├── requirements.txt
├── Dockerfile
└── sample_requests.json
```

## Lead scoring rules (deterministic)

Score components include:

- Budget tier (higher budget → higher points)
- Urgency (`high`, `medium`, `low`)
- Buying-intent keyword hits in message
- Company email quality (non-personal domain bonus)
- Message completeness (word count proxy)

### Classification thresholds

- `HOT`: score >= 70
- `WARM`: score >= 40
- `COLD`: score < 40

## AI response behavior

- Prompt includes lead context + classification
- AI output parsed as:
  - `Subject: ...`
  - `Message: ...`
- Message constrained to concise business style and expected under 120 words
- If formatting/API call fails, fallback response is returned

## Run locally

```bash
cd varynt-ai-lead-system
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
uvicorn app.main:app --reload
```

## Test

```bash
pytest -q
```

## Example API request

See `sample_requests.json`.

## Edge cases handled

- No budget provided (score still computed)
- Personal email domains reduce lead quality signal
- Sparse message content lowers completeness score
- AI timeout/error/invalid response format triggers fallback

## Production-aware choices (still lightweight)

- **Timeouts**: OpenAI client timeout configured in settings
- **Retries**: bounded retry loop for transient AI errors
- **Structured logs**: machine-parseable event names and metadata
- **Persistence**: in-memory SQLite for low overhead (replaceable later)
- **Modular boundaries**: easy to swap scoring rules or AI provider

## Scalability considerations

For growth, you can incrementally evolve without re-architecture:

1. Move from in-memory SQLite to Postgres.
2. Add async background queue for AI generation under heavy load.
3. Add idempotency keys + request tracing.
4. Add per-tenant scoring profiles.
5. Add evaluation harness to tune thresholds and keyword sets.

## Tradeoffs

- In-memory persistence is ephemeral (intentional MVP simplicity).
- Rule-based scoring is less adaptive than ML, but transparent and controllable.
- AI personalization is bounded and optional (system remains functional via fallback).
