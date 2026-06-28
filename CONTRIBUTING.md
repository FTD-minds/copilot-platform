# Contributing

Thanks for your interest in the Enterprise AI Copilot Platform.

## Development setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add a provider key
pytest -q
```

## Workflow
1. Create a branch: `feat/<short-name>` or `fix/<short-name>`.
2. Make focused commits with clear messages.
3. Ensure `ruff check .` and `pytest -q` pass locally.
4. Open a PR using the template; the CI **quality** and **eval-gate** jobs must pass.
5. New modules must follow the platform plugin contract (modules never import other modules).

## Engineering standards
- Every module ships with an eval suite (see `platform/evaluation/`).
- Add or update an ADR (`docs/adr/`) for any significant design decision.
- Keep secrets out of the repo; use `.env` (gitignored).

## Commit style
Conventional-ish: `type: summary` (e.g., `feat: add provider router`, `docs: ADR-002`).
