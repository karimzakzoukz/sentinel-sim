import json
import os

class SettingsLoader:
    """Loads application settings from a JSON file.

    The settings file path is taken from the SETTINGS_PATH environment variable.
    If the file does not exist or is malformed, a RuntimeError is raised.
    """

    def __init__(self):
        self.settings_path = os.getenv("SETTINGS_PATH", "config/settings.json")
        self.config = self._load_settings()

    def _load_settings(self) -> dict:
        """Read the JSON settings file and return a dict.

        Returns:
            dict: Parsed configuration.
        Raises:
            RuntimeError: If the file cannot be read or parsed.
        """
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise RuntimeError(f"Settings file not found: {self.settings_path}") from e
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Settings file is not valid JSON: {self.settings_path}") from e

        # Ensure required top‑level sections exist; provide sensible defaults for optional ones.
        # The 'database' section used to be mandatory; now we treat it as optional to maintain
        # backward compatibility with older settings files.
        data.setdefault("database", {})
        return data

    def get_database_config(self) -> dict:
        """Return the database configuration dictionary.

        Returns:
            dict: Database configuration (may be empty if not provided).
        """
        return self.config.get("database", {})

    # Additional helper methods can be added here for other config sections.

# Example usage (can be removed in production code):
# loader = SettingsLoader()
# db_cfg = loader.get_database_config()
