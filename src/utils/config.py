"""
Configuration management.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration."""

    # BLS API
    BLS_API_KEY = os.getenv('BLS_API_KEY', '')
    BLS_BASE_URL = 'https://api.bls.gov/publicAPI/v2'

    # Data paths
    DATA_RAW_DIR = os.getenv('DATA_RAW_DIR', 'data/raw')
    DATA_PROCESSED_DIR = os.getenv('DATA_PROCESSED_DIR', 'data/processed')

    # Scraping
    HEADLESS_BROWSER = os.getenv('HEADLESS_BROWSER', 'true').lower() == 'true'
    SCRAPE_INTERVAL_HOURS = int(os.getenv('SCRAPE_INTERVAL_HOURS', '24'))

    # Analysis
    ANALYSIS_LOOKBACK_DAYS = int(os.getenv('ANALYSIS_LOOKBACK_DAYS', '730'))
    CONFIDENCE_LEVEL = float(os.getenv('CONFIDENCE_LEVEL', '0.95'))

    @staticmethod
    def init_directories():
        """Initialize required directories."""
        Path(Config.DATA_RAW_DIR).mkdir(parents=True, exist_ok=True)
        Path(Config.DATA_PROCESSED_DIR).mkdir(parents=True, exist_ok=True)


def load_config():
    """Load and return configuration."""
    Config.init_directories()
    return Config
