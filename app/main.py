"""Sentinel-Sim — a tiny FastAPI service used as a Sentinel test target.

This is the CLEAN BASELINE. It works. It should never crash.

Bug variants live on separate branches:
  - bug/crashloop-typo  — typo in env var name → KeyError on startup
  - bug/oom             — allocates 100MB while limit is 32Mi → OOMKilled
  - bug/bad-config      — ConfigMap key mismatch → KeyError on first request
  - bug/bad-deploy      — bad image tag (chart-side bug, not app-side)

If you're reading this from `main`, the service is healthy.
"""
from __future__ import annotations

import os
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sentinel-sim")

app = FastAPI(title="sentinel-sim", version="1.0.0")


# ---- Config (read from env, with sensible defaults) ----
# On `bug/crashloop-typo` branch, this env var name is misspelled → app crashes.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sentinel-sim.db")
# Provide a default password to avoid KeyError if ConfigMap omits it.
DB_PASSWORD = os.environ.get("DB_PASSWORD", "default-password")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


@app.on_event("startup")
async def _startup() -> None:
    log.info("sentinel-sim starting up")
    log.info("DATABASE_URL=%s", DATABASE_URL)
    log.info("LOG_LEVEL=%s", LOG_LEVEL)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness probe — always returns 200 if the process is alive."""
    return {"status": "ok"}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    """Readiness probe — checks the app can serve traffic."""
    # Touch the config; using the default ensures no KeyError.
    _ = DB_PASSWORD
    return {"status": "ready", "database": DATABASE_URL}


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint — basic service info."""
    return {
        "service": "sentinel-sim",
        "version": "1.0.0",
        "description": "Sentinel test target — see README.md for the bug branches",
    }


@app.get("/pay")
async def pay(amount: int = 100) -> dict[str, str]:
    """Fake payment endpoint — used to generate traffic for Sentinel to monitor."""
    log.info("Processing payment amount=%s", amount)
    # On `bug/oom` branch, this allocates 100MB to trigger OOMKilled.
    # On main, we don't allocate anything.
    return {"status": "processed", "amount": str(amount)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
