import logging
from typing import Callable

from openai import OpenAI

from .config import settings

logger = logging.getLogger(__name__)


class AIClient:
    def __init__(self, client_factory: Callable[[], OpenAI] | None = None) -> None:
        self._client_factory = client_factory or (
            lambda: OpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout_seconds)
        )

    def generate_reply(self, prompt: str) -> str:
        last_error: Exception | None = None
        for attempt in range(settings.openai_max_retries + 1):
            try:
                client = self._client_factory()
                completion = client.chat.completions.create(
                    model=settings.openai_model,
                    temperature=0.4,
                    max_tokens=180,
                    messages=[
                        {
                            "role": "system",
                            "content": "You write concise, professional B2B outreach replies under 120 words.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                )
                return completion.choices[0].message.content or ""
            except Exception as exc:
                last_error = exc
                logger.warning("openai_retry", extra={"attempt": attempt + 1, "error": str(exc)})
        raise RuntimeError(f"OpenAI generation failed after retries: {last_error}")
