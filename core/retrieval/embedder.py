"""Embedding abstraction (mirrors the provider router pattern, ADR-003).

Default: a deterministic, dependency-free hashing embedder so retrieval runs in
CI and demos with no API keys. Production swaps in a real embedder
(OpenAI/Voyage/Bedrock) implementing the same interface — no other code changes.
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol, runtime_checkable

_DIM = 256
_token_re = re.compile(r"[a-z0-9]+")


@runtime_checkable
class Embedder(Protocol):
    name: str
    dim: int

    def embed(self, text: str) -> list[float]:
        ...


class HashingEmbedder:
    """Deterministic bag-of-tokens hashing embedder (no network, no key).

    Not semantically rich like a neural embedder, but stable and good enough to
    demonstrate the full RAG pipeline (chunk -> embed -> cosine search -> cite).
    """

    name = "hashing"
    dim = _DIM

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * _DIM
        for tok in _token_re.findall(text.lower()):
            h = int(hashlib.md5(tok.encode()).hexdigest(), 16)
            idx = h % _DIM
            sign = 1.0 if (h >> 8) & 1 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=False))


def get_embedder() -> Embedder:
    # Production: branch on config to return OpenAI/Voyage/Bedrock embedders.
    return HashingEmbedder()
