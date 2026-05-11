from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_qualify_endpoint_returns_shape():
    payload = {
        "full_name": "Alex Morgan",
        "email": "alex@varynt-client.com",
        "company": "Nimbus Labs",
        "budget_usd": 60000,
        "urgency": "medium",
        "message": "We are evaluating vendors and want a demo plus proposal in the next two weeks.",
    }
    res = client.post("/leads/qualify", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert "lead_score" in body
    assert body["classification"] in {"HOT", "WARM", "COLD"}
    assert "subject" in body["response"]
    assert "message" in body["response"]
