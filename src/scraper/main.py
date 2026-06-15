"""
Main data collection script.
Generates sample price data for demonstration.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from price_scraper import PriceScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Run the data collection pipeline."""

    logger.info("Starting price data collection...")

    # Initialize scraper
    project_root = Path(__file__).parent.parent.parent.parent
    data_raw = project_root / "data" / "raw"
    scraper = PriceScraper(output_dir=str(data_raw))

    # Generate sample data (replace with actual scraping in production)
    logger.info("Generating sample price data...")
    sample_data = scraper.get_sample_data()

    # Save data
    scraper.save_to_csv(sample_data, f"prices_{datetime.now().strftime('%Y%m%d')}.csv")

    logger.info(f"Successfully collected {len(sample_data)} price records")


if __name__ == "__main__":
    main()
