from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Urgency(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class LeadInput(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    company: str = Field(min_length=1, max_length=120)
    budget_usd: Optional[float] = Field(default=None, ge=0)
    urgency: Urgency = Urgency.medium
    message: str = Field(min_length=10, max_length=2000)


class LeadScoringResult(BaseModel):
    lead_score: int = Field(ge=0, le=100)
    classification: str


class AIResponse(BaseModel):
    subject: str
    message: str


class LeadOutput(BaseModel):
    lead_score: int
    classification: str
    response: AIResponse
