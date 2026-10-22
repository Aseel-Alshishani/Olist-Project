"""
Configuration Loader Module
Loads all paths and parameters dynamically from config/config.yaml
"""

from pathlib import Path
import yaml
from src.logger_config import setup_logger

logger = setup_logger()

class ConfigLoader:
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            self.config_path = Path("../config/config.yaml")
            
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Loads the YAML configuration file safely."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
                logger.info(f"Configuration successfully loaded from {self.config_path}")
                return config_data
        except Exception as e:
            logger.error(f"Failed to load configuration file: {e}")
            raise e

    def get_path(self, key: str) -> Path:
        """Retrieves a path from config and resolves it to an absolute Path object."""
        path_str = self.config["paths"][key]
        root = Path(__file__).resolve().parent.parent
        return root / path_str

    def get_parameter(self, section: str, key: str):
        """Retrieves a specific parameter value from the config."""
        return self.config[section][key]