# Milestone: Live Inference Verification

## Status: ✅ Integration Verified — ⏸️ External Quota Blocked
Date: Phase 1.5

## Summary
The model-agnostic provider router was exercised against the **real Anthropic API** end to end.
Authentication, environment-variable handling, provider routing, and the runtime all functioned correctly.
The only blocker is an **external Anthropic account usage/quota limit** (regains access 2026-07-01 00:00 UTC),
not an implementation defect.

## Verified
- `.env` loaded from project root (`copilot-platform/.env`), not `~/.env`.
- Anthropic API key loaded via `core/config.py`, **never logged or committed** (`.env` gitignored + untracked).
- Request reached Anthropic and **authenticated** (a 401 would indicate a bad key; we received a 400 quota error — proving auth succeeded).
- Router correctly selected `AnthropicProvider` from config; mock fallback preserved for keyless CI.

## Exact external error
```
anthropic.BadRequestError: 400 invalid_request_error
"You have reached your specified API usage limits. You will regain access on 2026-07-01 at 00:00 UTC."
request_id: req_011CcWcM8n2FY5C3EDKvX56C
```

## Resolution plan (no architecture change)
1. Restore Anthropic quota/billing (or supply an OpenAI key — router already supports it).
2. Rerun: `python scripts/verify_live_inference.py --provider anthropic`
3. Capture redacted metadata (provider/model/usage/latency) + close this milestone.

Development continues on the deterministic mock provider in the meantime (Phase 2 RAG).
