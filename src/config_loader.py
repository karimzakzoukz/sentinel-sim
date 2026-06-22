import os
import json
from typing import Any, Dict


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables and optional JSON config file.

    Returns a dictionary with all required configuration keys. Missing optional
    keys are given sensible defaults to avoid KeyError at runtime.
    """
    config: Dict[str, Any] = {}

    # Load from a JSON file if provided via CONFIG_PATH env var
    config_path = os.getenv("CONFIG_PATH")
    if config_path and os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                if isinstance(file_config, dict):
                    config.update(file_config)
        except Exception as e:
            # Log the error in real code; here we just ignore malformed files
            pass

    # Helper to fetch env var with optional default
    def env(key: str, default: Any = None) -> Any:
        return os.getenv(key, default)

    # Mandatory keys that previously caused KeyError – provide explicit defaults or raise clear error
    # LOKI_URL and JAEGER_URL are required for external services; if not set, keep None and let the caller handle it.
    config["LOKI_URL"] = env("LOKI_URL")
    config["JAEGER_URL"] = env("JAEGER_URL")

    # Other configuration values with sensible defaults
    config["SERVICE_PORT"] = int(env("SERVICE_PORT", "8080"))
    config["DEBUG_MODE"] = env("DEBUG_MODE", "false").lower() == "true"
    config["MAX_CONNECTIONS"] = int(env("MAX_CONNECTIONS", "100"))

    return config

# Expose a module‑level constant for easy import elsewhere
CONFIG = load_config()
