
"""
Configuration Loader Module.
Loads paths and parameters from config/config.yaml.
"""

from pathlib import Path

import yaml

from src.logger_config import setup_logger

logger = setup_logger(name=__name__)

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class ConfigLoader:
    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = PROJECT_ROOT / "config" / "config.yaml"
        else:
            self.config_path = Path(config_path)

            if not self.config_path.is_absolute():
                self.config_path = PROJECT_ROOT / self.config_path

        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load and validate the YAML configuration file."""

        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                config_data = yaml.safe_load(file)

            if not isinstance(config_data, dict):
                raise ValueError(
                    "Configuration file must contain a YAML dictionary."
                )

            logger.info(
                "Configuration successfully loaded from %s",
                self.config_path
            )

            return config_data

        except (OSError, yaml.YAMLError, ValueError):
            logger.exception(
                "Failed to load configuration from %s",
                self.config_path
            )
            raise

    def get_path(self, key: str) -> Path:
        """Get a project path as an absolute Path object."""

        paths = self.config.get("paths", {})

        if key not in paths:
            raise KeyError(f"Path '{key}' not found in configuration.")

        path = Path(paths[key])

        if not path.is_absolute():
            path = PROJECT_ROOT / path

        return path

    def get_parameter(self, section: str, key: str):
        """Get a parameter from a configuration section."""

        if section not in self.config:
            raise KeyError(
                f"Configuration section '{section}' not found."
            )

        if key not in self.config[section]:
            raise KeyError(
                f"Parameter '{key}' not found in section '{section}'."
            )

        return self.config[section][key]
