"""
BLS (Bureau of Labor Statistics) data integration module.
"""

import logging
import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BLSIntegration:
    """Handles integration with BLS API for CPI and economic data."""

    def __init__(self, api_key: str = ""):
        """
        Initialize BLS integration.

        Args:
            api_key: BLS API key (optional, higher rate limits with key)
        """
        self.api_key = api_key
        self.base_url = "https://api.bls.gov/publicAPI/v2"
        self.session = requests.Session()

    def get_cpi_data(self, series_id: str = "CPIAUCSL", start_year: int = 2022) -> pd.DataFrame:
        """
        Retrieve CPI data from BLS.

        Args:
            series_id: BLS series ID (CPIAUCSL = All Items CPI-U)
            start_year: Starting year for data retrieval

        Returns:
            DataFrame with CPI data
        """
        try:
            end_year = datetime.now().year
            years = list(range(start_year, end_year + 1))

            # BLS API allows up to 20 years per request
            all_data = []

            for i in range(0, len(years), 20):
                year_batch = years[i:i+20]

                payload = {
                    'seriesid': [series_id],
                    'startyear': str(year_batch[0]),
                    'endyear': str(year_batch[-1]),
                    'registrationkey': self.api_key
                }

                response = self.session.post(
                    f"{self.base_url}/timeseries/data",
                    json=payload,
                    headers={'Content-type': 'application/json'}
                )

                if response.status_code == 200:
                    data = response.json()

                    if 'Results' in data and 'series' in data['Results']:
                        for series in data['Results']['series']:
                            for item in series['data']:
                                all_data.append({
                                    'year': int(item['year']),
                                    'period': item['period'],
                                    'cpi_value': float(item['value']),
                                    'footnotes': item.get('footnotes', [])
                                })

            df = pd.DataFrame(all_data)

            # Create proper date column (periods are M01-M12 for months)
            df['month'] = df['period'].str.replace('M', '').astype(int)
            df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

            return df[['date', 'cpi_value']].sort_values('date')

        except Exception as e:
            logger.error(f"Error retrieving CPI data: {e}")
            return pd.DataFrame()

    def get_employment_data(self, state_fips: str = "00") -> pd.DataFrame:
        """
        Retrieve employment data from BLS.

        Args:
            state_fips: State FIPS code (00 = US total)

        Returns:
            DataFrame with employment data
        """
        # SMS01000000000000001 = Total nonfarm employment for US
        series_id = f"SMS{state_fips}000000000000001"

        try:
            payload = {
                'seriesid': [series_id],
                'startyear': '2022',
                'endyear': str(datetime.now().year),
                'registrationkey': self.api_key
            }

            response = self.session.post(
                f"{self.base_url}/timeseries/data",
                json=payload,
                headers={'Content-type': 'application/json'}
            )

            if response.status_code == 200:
                data = response.json()
                employment_data = []

                if 'Results' in data and 'series' in data['Results']:
                    for series in data['Results']['series']:
                        for item in series['data']:
                            employment_data.append({
                                'year': int(item['year']),
                                'period': item['period'],
                                'employment': int(item['value'])
                            })

                df = pd.DataFrame(employment_data)
                df['month'] = df['period'].str.replace('M', '').astype(int)
                df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

                return df[['date', 'employment']].sort_values('date')

            return pd.DataFrame()

        except Exception as e:
            logger.error(f"Error retrieving employment data: {e}")
            return pd.DataFrame()

    def get_sample_cpi_data(self) -> pd.DataFrame:
        """Generate sample CPI data for testing."""
        import numpy as np

        dates = pd.date_range(start='2022-01-01', periods=24, freq='MS')
        # Simulate realistic CPI values (base 100 in 1982-84)
        base_cpi = 290
        cpi_values = base_cpi + np.cumsum(np.random.normal(1, 0.5, len(dates)))

        return pd.DataFrame({
            'date': dates,
            'cpi_value': cpi_values.round(2)
        })


if __name__ == "__main__":
    bls = BLSIntegration()
    sample_cpi = bls.get_sample_cpi_data()
    print(sample_cpi)
