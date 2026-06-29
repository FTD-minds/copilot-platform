"""Platform API — FastAPI gateway exposing health, provider info, and chat.

This is the model-agnostic entrypoint: the /chat endpoint works with any
configured provider (mock by default, Anthropic/OpenAI when keys are set).
"""
from __future__ import annotations

import logging

from fastapi import FastAPI
from pydantic import BaseModel

from core.config import get_settings
from core.providers.base import ChatMessage
from core.providers.router import available_providers, get_provider

logging.basicConfig(level=get_settings().log_level)
logger = logging.getLogger("copilot.api")

app = FastAPI(
    title="Enterprise AI Copilot Platform",
    description="Model-agnostic platform API. Module 1: ERP Sync Reconciliation Copilot.",
    version="0.1.0",
)


class ChatTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatTurn]
    provider: str | None = None
    model: str | None = None


class ChatReply(BaseModel):
    text: str
    provider: str
    model: str
    usage: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "copilot-platform", "version": app.version}


@app.get("/providers")
def providers() -> dict:
    return {"available": available_providers()}


@app.post("/chat", response_model=ChatReply)
def chat(req: ChatRequest) -> ChatReply:
    provider = get_provider(req.provider)
    logger.info("chat.request provider=%s model=%s turns=%d", provider.name, req.model, len(req.messages))
    resp = provider.complete(
        [ChatMessage(role=t.role, content=t.content) for t in req.messages],
        model=req.model,
    )
    logger.info("chat.response provider=%s model=%s out_tokens=%s",
                resp.provider, resp.model, resp.usage.get("output_tokens"))
    return ChatReply(text=resp.text, provider=resp.provider, model=resp.model, usage=resp.usage)
