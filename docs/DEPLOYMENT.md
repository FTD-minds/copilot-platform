# DEPLOYMENT RUNBOOK — Public URL in ~5 minutes

The platform is container-ready and runs **fully on the mock provider with no API keys**, so the public demo works immediately and costs $0.

## Option A — Render (recommended, no CLI, free)
1. Go to https://render.com → sign up / log in with GitHub.
2. **New → Web Service** → connect the `FTD-minds/copilot-platform` repo.
3. Render detects `render.yaml` (Docker). Click **Apply / Create**.
4. Wait ~3–5 min for the build. You get a stable URL like `https://copilot-platform-XXXX.onrender.com`.
5. Verify (see checklist below).

> Note: Render free tier sleeps after inactivity (~50s cold start). Fine for a portfolio demo; mention it in the README so reviewers aren't surprised, or upgrade to the $7/mo plan for always-on.

## Option B — Fly.io (CLI, always-on free allowance)
```bash
brew install flyctl && flyctl auth login
cd ~/Desktop/ProjectHermes/copilot-platform
flyctl launch --copy-config --name copilot-platform --now   # uses the Dockerfile
```

## Option C — Railway (web, simple)
railway.app → New Project → Deploy from GitHub repo → select repo → it builds the Dockerfile.

## POST-DEPLOY VERIFICATION (production end-to-end)
Replace BASE with your live URL:
```bash
curl -s BASE/health                      # {"status":"ok"...}
curl -s BASE/providers                   # {"available":{"mock":true,...}}
curl -s BASE/api/evals | python3 -m json.tool   # passing:true, 4 metrics
curl -s -X POST BASE/modules/erp-sync/agent-diagnose \
  -H 'content-type: application/json' \
  -d '{"query":"stripe payout does not match deposit","inputs":{"gross_payments":[600,400],"processor_fees":0,"bank_deposit":970}}'
# expect: steps [plan,retrieve,reconciliation_calculator], discrepancy -30.0, citations [kb-003,...]
```
Open `BASE/` in a browser → the Diagnose console + Eval Dashboard should load.

## AFTER IT'S LIVE — tell me the URL and I will:
- Insert it into README (live-demo badge + section), portfolio site, LinkedIn, all 3 resumes
- Flip M-01 from 0 → 1 and cut Master Resume v1.0
- Update the recruiter walkthrough with the clickable link
