import os
import json

# Default configuration path if environment variable is missing
DEFAULT_CONFIG_PATH = "/etc/sentinel/config.json"

def load_config():
    """Load configuration from the path specified by the environment variable
    SENTINEL_CONFIG_PATH. If the variable is not set, fall back to
    DEFAULT_CONFIG_PATH. If the file does not exist, raise a clear error.
    """
    config_path = os.getenv("SENTINEL_CONFIG_PATH", DEFAULT_CONFIG_PATH)
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found at '{config_path}'. "
            "Please set the SENTINEL_CONFIG_PATH environment variable or "
            "ensure the default config exists."
        )
    with open(config_path, "r") as f:
        return json.load(f)

# Expose a module-level config object for convenience
try:
    CONFIG = load_config()
except Exception as e:
    # Log the error and exit gracefully
    import logging
    logging.error(e)
    raise
