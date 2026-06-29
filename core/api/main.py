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
from modules.erp_sync_reconciliation.service import ReconciliationCopilot

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


class DiagnoseRequest(BaseModel):
    query: str
    k: int = 3
    provider: str | None = None
    model: str | None = None


class CitationModel(BaseModel):
    id: str
    title: str
    score: float


class DiagnoseReply(BaseModel):
    answer: str
    citations: list[CitationModel]
    provider: str
    model: str


class AgentDiagnoseRequest(BaseModel):
    query: str
    inputs: dict = {}


class AgentDiagnoseReply(BaseModel):
    answer: str
    steps: list[dict]
    citations: list[str]
    tool_outputs: dict


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


# --- Module 1: ERP Sync Reconciliation Copilot ---
_copilot: ReconciliationCopilot | None = None


def _get_copilot() -> ReconciliationCopilot:
    global _copilot
    if _copilot is None:
        _copilot = ReconciliationCopilot()
    return _copilot


@app.post("/modules/erp-sync/diagnose", response_model=DiagnoseReply)
def diagnose(req: DiagnoseRequest) -> DiagnoseReply:
    copilot = _get_copilot()
    result = copilot.diagnose(req.query, k=req.k, provider=req.provider, model=req.model)
    logger.info("diagnose provider=%s model=%s citations=%d",
                result.provider, result.model, len(result.citations))
    return DiagnoseReply(
        answer=result.answer,
        citations=[CitationModel(id=c.id, title=c.title, score=c.score) for c in result.citations],
        provider=result.provider,
        model=result.model,
    )


@app.post("/modules/erp-sync/agent-diagnose", response_model=AgentDiagnoseReply)
def agent_diagnose(req: AgentDiagnoseRequest) -> AgentDiagnoseReply:
    from core.retrieval.store import InMemoryVectorStore
    from modules.erp_sync_reconciliation.agents.diagnostic_agent import DiagnosticAgent
    from modules.erp_sync_reconciliation.service import load_kb

    store = InMemoryVectorStore()
    store.add(load_kb())
    agent = DiagnosticAgent(store)
    result = agent.run(req.query, inputs=req.inputs)
    logger.info("agent.diagnose steps=%d tools=%s", len(result.steps), list(result.tool_outputs))
    return AgentDiagnoseReply(
        answer=result.answer,
        steps=[{"name": s.name, "detail": s.detail} for s in result.steps],
        citations=result.citations,
        tool_outputs=result.tool_outputs,
    )
