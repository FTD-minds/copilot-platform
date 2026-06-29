"""ERP Sync Reconciliation Copilot — RAG diagnose service.

Loads the module knowledge base, retrieves the most relevant entries for a
described sync/reconciliation failure, and produces a grounded, cited answer
via the model-agnostic provider router. With the mock provider this returns a
deterministic grounded summary; with a real provider it produces a natural
explanation constrained to the retrieved context.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from core.providers.base import ChatMessage
from core.providers.router import get_provider
from core.retrieval.store import Document, InMemoryVectorStore

_KB_PATH = Path(__file__).parent / "knowledge" / "kb.json"


@dataclass
class Citation:
    id: str
    title: str
    score: float


@dataclass
class Diagnosis:
    answer: str
    citations: list[Citation]
    provider: str
    model: str


def load_kb(path: Path = _KB_PATH) -> list[Document]:
    raw = json.loads(path.read_text())
    return [Document(id=d["id"], title=d["title"], text=d["text"], category=d.get("category", "")) for d in raw]


class ReconciliationCopilot:
    def __init__(self, store: InMemoryVectorStore | None = None) -> None:
        self._store = store or InMemoryVectorStore()
        if len(self._store) == 0:
            self._store.add(load_kb())

    def _system_prompt(self, context: str) -> str:
        return (
            "You are an ERP sync & reconciliation diagnostic assistant. "
            "Answer ONLY using the provided knowledge context. "
            "Cite the knowledge entry IDs you used in brackets like [kb-001]. "
            "If the context does not cover the issue, say so.\n\n"
            f"KNOWLEDGE CONTEXT:\n{context}"
        )

    def diagnose(self, query: str, k: int = 3, provider: str | None = None,
                 model: str | None = None) -> Diagnosis:
        hits = self._store.search(query, k=k)
        context = "\n\n".join(f"[{h.doc.id}] {h.doc.title}: {h.doc.text}" for h in hits)
        citations = [Citation(id=h.doc.id, title=h.doc.title, score=round(h.score, 4)) for h in hits]

        prov = get_provider(provider)
        resp = prov.complete(
            [
                ChatMessage(role="system", content=self._system_prompt(context)),
                ChatMessage(role="user", content=query),
            ],
            model=model,
        )

        # With the mock provider, synthesize a deterministic grounded answer so the
        # pipeline is demonstrable without a live model.
        if prov.name == "mock":
            top = hits[0].doc if hits else None
            if top is not None:
                answer = (
                    f"Most likely cause: {top.title}. {top.text} "
                    f"[{top.id}]"
                )
            else:
                answer = "No relevant knowledge entry found for this issue."
        else:
            answer = resp.text

        return Diagnosis(answer=answer, citations=citations, provider=resp.provider, model=resp.model)
