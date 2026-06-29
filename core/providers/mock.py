"""Mock provider: deterministic, no network, no API key.

Lets the platform run in CI and local demos without secrets, and gives tests a
stable target. Real adapters (Anthropic/OpenAI) share the same interface.
"""
from __future__ import annotations

from .base import ChatMessage, ChatResponse, Provider


class MockProvider:
    name = "mock"

    def complete(self, messages: list[ChatMessage], *, model: str | None = None) -> ChatResponse:
        last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        text = f"[mock:{model or 'mock-1'}] received {len(messages)} message(s). echo: {last_user}"
        return ChatResponse(
            text=text,
            provider=self.name,
            model=model or "mock-1",
            usage={"input_tokens": sum(len(m.content) for m in messages), "output_tokens": len(text)},
        )


_provider: Provider = MockProvider()
