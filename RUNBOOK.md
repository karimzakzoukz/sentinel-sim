# Sentinel-Sim Runbook

This runbook covers the incidents that the `sentinel-sim` service is designed
to trigger. Sentinel uses this runbook URL (from the `sentinel.io/runbook`
annotation on the Deployment) as context during investigations.

## Service overview

- **What it does**: Simple HTTP health-check + payment-processing stub
- **Criticality**: Medium (test environment — not real money)
- **Owning team**: payments
- **Repo**: https://github.com/karimzakzoukz/sentinel-sim
- **SLA**: 99% uptime in business hours (this is a test target, relax)

## Known incident patterns

### CrashLoopBackOff (env var typo)

**Symptoms**: Pod restarts every ~10s, never becomes Ready.
**Logs**: `KeyError: 'DATABASE_URL'` or similar.
**Cause**: A typo in the env var name in `values.yaml` or `app/main.py`.
**Fix**: Align the env var name between the chart and the app code.

### OOMKilled

**Symptoms**: Pod restarts every ~30s. Last log line is mid-request.
**Logs**: No error — pod is killed by the kernel before it can log.
**Cause**: Memory limit too low for the workload, OR a memory leak in the app.
**Fix**: If a recent deploy reduced the limit, restore it. If the app started
leaking, profile + fix the leak. Sentinel should propose bumping the memory
limit as the immediate fix.

### Bad image tag (ImagePullBackOff)

**Symptoms**: Pod never starts. `kubectl describe pod` shows
`Failed to pull image "karimzakzoukz/sentinel-sim:TYPO"`.
**Cause**: A typo in the image tag in `values.yaml`.
**Fix**: Correct the tag to match an existing image on the registry.

### ConfigMap key mismatch

**Symptoms**: Pod starts but crashes on first request.
**Logs**: `KeyError: 'DB_PASSWORD'` when reading the config.
**Cause**: The app expects `DB_PASSWORD` but the ConfigMap has `db_password`.
**Fix**: Align the keys (camelCase vs snake_case).

## Escalation

If Sentinel cannot auto-fix within 5 minutes, page the payments on-call.
