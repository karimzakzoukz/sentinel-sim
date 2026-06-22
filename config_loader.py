import os
import yaml


def load_config():
    """Load the sentinel configuration.

    The original implementation expected the environment variable
    ``SENTINEL_CONFIG_PATH`` to be set and accessed it via
    ``os.environ['SENTINEL_CONFIG_PATH']``.  When the variable was missing a
    ``KeyError`` was raised during container start‑up, causing the pod to
    crash.  The new implementation uses ``os.getenv`` with a sensible
    default path (``/etc/sentinel/config.yaml``) so that the service can
    start even if the variable is omitted.  The default path should be
    populated by the image or the deployment configuration.
    """
    config_path = os.getenv('SENTINEL_CONFIG_PATH', '/etc/sentinel/config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
