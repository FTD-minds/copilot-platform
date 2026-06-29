"""Anthropic adapter. SDK imported lazily so the dependency is optional."""
from __future__ import annotations

from .base import ChatMessage, ChatResponse


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, api_key: str, default_model: str = "claude-3-5-sonnet-latest") -> None:
        self._api_key = api_key
        self._default_model = default_model

    def complete(self, messages: list[ChatMessage], *, model: str | None = None) -> ChatResponse:
        import anthropic  # lazy

        client = anthropic.Anthropic(api_key=self._api_key)
        system = "\n".join(m.content for m in messages if m.role == "system") or None
        convo = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role in ("user", "assistant")
        ]
        used_model = model or self._default_model
        resp = client.messages.create(
            model=used_model, max_tokens=1024, system=system or "", messages=convo  # type: ignore[arg-type]
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"  # type: ignore[attr-defined]
        )
        return ChatResponse(
            text=text,
            provider=self.name,
            model=used_model,
            usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
        )
