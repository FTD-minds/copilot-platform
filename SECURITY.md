# Security Policy

## Reporting a vulnerability
Please open a private security advisory via GitHub ("Security" tab → "Report a vulnerability"),
or email senaymesfin20@gmail.com. Do not open public issues for security reports.

## Scope & posture
- **No real customer data.** All sample ERP data in `data/sample_erp/` is synthetic and PII-free.
- **Secrets** are provided via environment variables / secret stores, never committed.
- **Input validation** on all API boundaries (Pydantic).
- **Authorization** enforced on platform endpoints.
- **Dependency scanning** runs in CI.
- **Retrieval/prompt-injection:** retrieved content is treated as untrusted; the orchestration layer
  applies guardrails and never executes instructions embedded in retrieved documents.

## Supported versions
The `main` branch receives security updates during active development.
