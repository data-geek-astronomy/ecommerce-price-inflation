"""
Web scraping module for collecting e-commerce price data.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PriceScraper:
    """Scrapes price data from e-commerce platforms."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_amazon(self, product_asin: str, category: str) -> Optional[Dict]:
        """
        Scrape product price from Amazon.

        Args:
            product_asin: Amazon Standard Identification Number
            category: Product category (e.g., 'Electronics', 'Books')

        Returns:
            Dictionary with product data or None if failed
        """
        try:
            url = f"https://www.amazon.com/dp/{product_asin}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract price (Note: Amazon structure changes, may need updates)
            price_elem = soup.find('span', class_='a-price-whole')
            if not price_elem:
                logger.warning(f"Could not find price for {product_asin}")
                return None

            price_text = price_elem.get_text(strip=True).replace('$', '').replace(',', '')

            return {
                'timestamp': datetime.now().isoformat(),
                'platform': 'Amazon',
                'product_id': product_asin,
                'category': category,
                'price': float(price_text),
                'currency': 'USD'
            }

        except Exception as e:
            logger.error(f"Error scraping Amazon product {product_asin}: {e}")
            return None

    def save_to_csv(self, data: List[Dict], filename: str = "price_data.csv"):
        """Save scraped data to CSV file."""
        filepath = self.output_dir / filename

        if not data:
            logger.warning("No data to save")
            return

        try:
            with open(filepath, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())

                # Write header only if file is empty
                if filepath.stat().st_size == 0:
                    writer.writeheader()

                writer.writerows(data)

            logger.info(f"Saved {len(data)} records to {filepath}")

        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}")

    def get_sample_data(self) -> List[Dict]:
        """
        Generate sample price data for testing.
        This will be replaced with actual scraping.
        """
        import random
        from datetime import datetime, timedelta

        categories = ['Electronics', 'Home & Garden', 'Sports', 'Books', 'Fashion']
        platforms = ['Amazon', 'Best Buy', 'Walmart']

        sample_data = []
        base_date = datetime.now() - timedelta(days=180)

        for day in range(180):
            current_date = base_date + timedelta(days=day)
            for _ in range(5):  # 5 products per day
                price = random.uniform(20, 500)
                sample_data.append({
                    'timestamp': current_date.isoformat(),
                    'platform': random.choice(platforms),
                    'product_id': f"PROD_{random.randint(1000, 9999)}",
                    'category': random.choice(categories),
                    'price': round(price, 2),
                    'currency': 'USD'
                })

        return sample_data


if __name__ == "__main__":
    scraper = PriceScraper()
    sample = scraper.get_sample_data()
    scraper.save_to_csv(sample)
    print(f"Generated {len(sample)} sample price records")
