"""Model-agnostic provider abstraction.

A `Provider` turns a list of chat messages into a `ChatResponse`. Concrete
adapters (Anthropic, OpenAI, Bedrock, Vertex, Mock) implement the same interface
so the rest of the platform never depends on a specific vendor (see ADR-002).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class ChatMessage:
    role: str   # "system" | "user" | "assistant"
    content: str


@dataclass
class ChatResponse:
    text: str
    provider: str
    model: str
    usage: dict = field(default_factory=dict)


@runtime_checkable
class Provider(Protocol):
    name: str

    def complete(self, messages: list[ChatMessage], *, model: str | None = None) -> ChatResponse:
        ...
