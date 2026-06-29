"""Vector store + retriever.

In-memory cosine store for the hermetic vertical slice; pgvector is the
production target (same interface). See ADR-003.
"""
from __future__ import annotations

from dataclasses import dataclass

from .embedder import Embedder, cosine, get_embedder


@dataclass
class Document:
    id: str
    title: str
    text: str
    category: str = ""


@dataclass
class RetrievedChunk:
    doc: Document
    score: float


class InMemoryVectorStore:
    def __init__(self, embedder: Embedder | None = None) -> None:
        self._embedder = embedder or get_embedder()
        self._items: list[tuple[Document, list[float]]] = []

    def add(self, docs: list[Document]) -> None:
        for d in docs:
            self._items.append((d, self._embedder.embed(f"{d.title}. {d.text}")))

    def search(self, query: str, k: int = 3) -> list[RetrievedChunk]:
        q = self._embedder.embed(query)
        scored = [RetrievedChunk(doc=d, score=cosine(q, v)) for d, v in self._items]
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:k]

    def __len__(self) -> int:
        return len(self._items)
