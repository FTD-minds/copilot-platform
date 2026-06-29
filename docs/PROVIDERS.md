# Provider Setup Guide

The platform is **model-agnostic** (see [ADR-002](./adr/ADR-002-model-agnostic-provider-abstraction.md)).
Choosing a provider is a configuration concern, never a code change. Secrets are read from
environment variables (or a gitignored `.env`) via `core/config.py` and are **never logged or committed**.

## Secure key handling
- Keys live only in `.env` (gitignored) or your shell/secret manager — never in source.
- `Settings` (pydantic-settings) loads them at runtime; the app logs provider/model/usage **but never the key**.
- CI runs with **no keys** using the deterministic mock provider (hermetic builds).

## Anthropic (active option)
```bash
export ANTHROPIC_API_KEY=sk-ant-...
export LLM_PROVIDER=anthropic
export LLM_MODEL=claude-3-5-sonnet-latest
python scripts/verify_live_inference.py --provider anthropic
```

## OpenAI (active option)
```bash
export OPENAI_API_KEY=sk-...
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o-mini
python scripts/verify_live_inference.py --provider openai
```

## Adding future providers
The contract is `core/providers/base.py::Provider` — implement `complete(messages, model) -> ChatResponse`.

### AWS Bedrock (planned)
1. `pip install boto3`; create `core/providers/bedrock_provider.py` implementing `Provider`.
2. Auth via standard AWS credentials (env/role); region from `AWS_BEDROCK_REGION`.
3. Register in `router.get_provider()` under `name == "bedrock"`.

### Google Vertex AI (planned)
1. `pip install google-cloud-aiplatform`; create `core/providers/vertex_provider.py`.
2. Auth via Application Default Credentials; project from `GOOGLE_VERTEX_PROJECT`.
3. Register in `router.get_provider()` under `name == "vertex"`.

No module or API change is required to add a provider — only a new adapter + one router branch.
