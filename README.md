# Sentinel Simulation Target

A small Python web service used to **test Sentinel end-to-end**. It has
intentional bugs that trigger different K8s incident types when deployed.

## What this is for

This repo is the **target** for Sentinel to monitor and fix. The workflow:

1. You install Sentinel into a K8s cluster.
2. You deploy this service into the same cluster using the included Helm chart.
3. You push broken code on a branch and merge to `main`.
4. CI builds + deploys the broken version.
5. The service starts crashing (CrashLoopBackOff, OOMKilled, etc.).
6. Sentinel detects the incident, investigates, opens a PR back to THIS repo
   with the fix.
7. You merge the PR — service recovers. End-to-end autonomous remediation
   complete.

## The intentional bugs

Each branch in this repo introduces a different bug for Sentinel to find:

| Branch | Bug | Expected Sentinel behavior |
|--------|-----|----------------------------|
| `main` | Clean baseline (works) | No incidents |
| `bug/crashloop-typo` | Typo in env var name → app crashes on startup | Investigator finds the typo, Fix Proposer opens PR fixing it |
| `bug/oom` | Memory limit reduced to 32Mi, app allocates 100MB → OOMKilled | Investigator finds OOM pattern, Fix Proposer bumps memory in values.yaml |
| `bug/bad-config` | ConfigMap key mismatch → app can't read DB password | Investigator spots the mismatch, Fix Proposer aligns the keys |
| `bug/bad-deploy` | Bad image tag (typo in chart's image.tag) → ImagePullBackOff | Investigator finds the bad tag, Fix Proposer fixes values.yaml |

## Annotation contract

The Helm chart in this repo annotates every Deployment with:

```yaml
metadata:
  annotations:
    sentinel.io/repo: "karimzakzoukz/sentinel-sim"
    sentinel.io/team: "payments"
    sentinel.io/runbook: "https://github.com/karimzakzoukz/sentinel-sim/blob/main/RUNBOOK.md"
```

This is how Sentinel's Fix Proposer knows where to open the PR. Without this
annotation, Sentinel will detect + investigate but cannot autonomously fix.

## Local development

```bash
# Run the service locally
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Run the broken version (switch branches first)
git checkout bug/crashloop-typo
uvicorn app.main:app --reload --port 8000  # crashes immediately
```

## License

MIT — this is a test target, do whatever you want with it.
