"""Sentinel-Sim — a tiny FastAPI service used as a Sentinel test target.

BUG variant: bug/runtime-divzero
  - The /pay endpoint divides by `amount` without checking for zero
  - Calling /pay?amount=0 triggers ZeroDivisionError → 500 response
  - The pod stays Running (no CrashLoopBackOff) — this is a RUNTIME bug
  - Sentinel must read the pod logs (current, not previous) to see the error
"""
from __future__ import annotations

import os
import logging
from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sentinel-sim")

app = FastAPI(title="sentinel-sim", version="1.0.0")


# ---- Config (read from env, with sensible defaults) ----
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sentinel-sim.db")
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
    """Fake payment endpoint — now validates amount to avoid division by zero."""
    log.info("Processing payment amount=%s", amount)
    if amount == 0:
        # Return a client error instead of crashing
        raise HTTPException(status_code=400, detail="Amount must be non-zero")
    fee = amount / amount
    return {"status": "processed", "amount": str(amount), "fee": str(fee)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
