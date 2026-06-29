"""OpenAI adapter. SDK imported lazily so the dependency is optional."""
from __future__ import annotations

from .base import ChatMessage, ChatResponse


class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key: str, default_model: str = "gpt-4o-mini") -> None:
        self._api_key = api_key
        self._default_model = default_model

    def complete(self, messages: list[ChatMessage], *, model: str | None = None) -> ChatResponse:
        from openai import OpenAI  # lazy

        client = OpenAI(api_key=self._api_key)
        used_model = model or self._default_model
        resp = client.chat.completions.create(
            model=used_model,
            messages=[{"role": m.role, "content": m.content} for m in messages],  # type: ignore[misc]
        )
        text = resp.choices[0].message.content or ""
        usage = getattr(resp, "usage", None)
        return ChatResponse(
            text=text,
            provider=self.name,
            model=used_model,
            usage={
                "input_tokens": getattr(usage, "prompt_tokens", 0),
                "output_tokens": getattr(usage, "completion_tokens", 0),
            },
        )
