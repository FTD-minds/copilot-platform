"""Verify a real end-to-end AI inference path through the model-agnostic router.

Usage:
    # set a key first (never committed):
    export ANTHROPIC_API_KEY=sk-ant-...      # or OPENAI_API_KEY=sk-...
    python scripts/verify_live_inference.py --provider anthropic

Prints request/response METADATA only. Never prints the API key. Response text
is shown so you can confirm a real model answered; keys are redacted everywhere.
"""
from __future__ import annotations

import argparse
import time

from core.providers.base import ChatMessage
from core.providers.router import available_providers, get_provider


def _redact(env_present: dict[str, bool]) -> dict[str, str]:
    return {k: ("set" if v else "absent") for k, v in env_present.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default=None, help="anthropic | openai | mock")
    parser.add_argument("--model", default=None)
    parser.add_argument(
        "--prompt",
        default="In one sentence, why might a QuickBooks Online deposit fail to reconcile against a bank feed?",
    )
    args = parser.parse_args()

    avail = available_providers()
    print(f"[verify] provider availability: {_redact(avail)}")

    provider = get_provider(args.provider)
    print(f"[verify] selected provider: {provider.name}")
    if provider.name == "mock" and args.provider in ("anthropic", "openai"):
        print(f"[verify] WARNING: requested '{args.provider}' but no key present -> fell back to mock.")
        print("[verify] Set ANTHROPIC_API_KEY or OPENAI_API_KEY and re-run for real inference.")

    t0 = time.perf_counter()
    resp = provider.complete([ChatMessage(role="user", content=args.prompt)], model=args.model)
    latency_ms = round((time.perf_counter() - t0) * 1000, 1)

    print("[verify] --- request metadata ---")
    print(f"  prompt_chars={len(args.prompt)} provider={provider.name} model={args.model or 'default'}")
    print("[verify] --- response metadata ---")
    print(f"  provider={resp.provider} model={resp.model} usage={resp.usage} latency_ms={latency_ms}")
    print("[verify] --- response text ---")
    print(f"  {resp.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
