"""Provider router — selects a provider by config/name (ADR-002).

The platform calls `get_provider()`; it never imports a vendor SDK directly.
Falls back to the mock provider when a requested provider has no API key, so
the system always runs (CI, demos) and degrades gracefully.
"""
from __future__ import annotations

from core.config import Settings, get_settings

from .base import Provider
from .mock import MockProvider


def get_provider(name: str | None = None, settings: Settings | None = None) -> Provider:
    settings = settings or get_settings()
    name = (name or settings.llm_provider).lower()

    if name == "anthropic" and settings.anthropic_api_key:
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider(settings.anthropic_api_key, settings.llm_model)

    if name == "openai" and settings.openai_api_key:
        from .openai_provider import OpenAIProvider
        return OpenAIProvider(settings.openai_api_key, settings.llm_model)

    # Default / graceful fallback.
    return MockProvider()


def available_providers(settings: Settings | None = None) -> dict[str, bool]:
    settings = settings or get_settings()
    return {
        "mock": True,
        "anthropic": bool(settings.anthropic_api_key),
        "openai": bool(settings.openai_api_key),
    }
