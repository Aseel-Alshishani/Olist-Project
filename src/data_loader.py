"""
Data Loader Module
Responsible for safe data ingestion from various sources (CSV, Database, etc.)
"""

from pathlib import Path
import pandas as pd
from src.logger_config import setup_logger

logger = setup_logger(name=__name__)

class DataLoader:
    @staticmethod
    def load_csv(file_path: Path) -> pd.DataFrame:
        """
        Loads raw data from a CSV file with memory optimization.
        """
        if not file_path.exists():
            logger.error(f"File not found at path: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logger.info(f"Successfully loaded data from {file_path}")
        return pd.read_csv(file_path, low_memory=False)