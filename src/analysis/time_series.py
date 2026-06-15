"""
Time series analysis module for price data.
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Tuple, Dict

import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TimeSeriesAnalysis:
    """Performs time series analysis on price data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with price data.

        Args:
            df: DataFrame with columns: timestamp, category, price
        """
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp')
        self.decompositions = {}

    def calculate_price_trends(self, window: int = 30) -> pd.DataFrame:
        """
        Calculate price trends using moving averages.

        Args:
            window: Window size for moving average (days)

        Returns:
            DataFrame with trend analysis
        """
        trends = []

        for category in self.df['category'].unique():
            cat_data = self.df[self.df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()

            # Calculate moving averages
            sma = cat_data.rolling(window=window).mean()
            ema = cat_data.ewm(span=window).mean()

            # Calculate momentum
            momentum = cat_data.pct_change(window)

            trends.append({
                'category': category,
                'latest_price': cat_data.iloc[-1],
                'ma_30': sma.iloc[-1],
                'ema_30': ema.iloc[-1],
                'momentum': momentum.iloc[-1],
                'avg_price': cat_data.mean(),
                'price_volatility': cat_data.std()
            })

        return pd.DataFrame(trends)

    def decompose_series(self, category: str, period: int = 30) -> Dict:
        """
        Decompose price series into trend, seasonal, and residual components.

        Args:
            category: Product category
            period: Seasonal period (days)

        Returns:
            Dictionary with decomposition components
        """
        cat_data = self.df[self.df['category'] == category].copy()
        cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()

        # Fill missing values
        cat_data = cat_data.fillna(method='ffill').fillna(method='bfill')

        if len(cat_data) < 2 * period:
            logger.warning(f"Not enough data for {category} to decompose with period {period}")
            return {}

        try:
            decomposition = seasonal_decompose(cat_data, model='additive', period=period)

            self.decompositions[category] = {
                'original': cat_data,
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid
            }

            return self.decompositions[category]

        except Exception as e:
            logger.error(f"Error decomposing {category}: {e}")
            return {}

    def test_stationarity(self, category: str) -> Dict:
        """
        Perform Augmented Dickey-Fuller test for stationarity.

        Args:
            category: Product category

        Returns:
            Dictionary with test results
        """
        cat_data = self.df[self.df['category'] == category].copy()
        cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()
        cat_data = cat_data.dropna()

        if len(cat_data) < 10:
            return {'error': 'Not enough data for stationarity test'}

        try:
            result = adfuller(cat_data, autolag='AIC')

            return {
                'category': category,
                'adf_statistic': result[0],
                'p_value': result[1],
                'n_lags': result[2],
                'is_stationary': result[1] < 0.05,
                'critical_values': result[4]
            }
        except Exception as e:
            logger.error(f"Error testing stationarity for {category}: {e}")
            return {'error': str(e)}

    def calculate_inflation_rate(self, window: int = 7) -> pd.DataFrame:
        """
        Calculate week-over-week inflation rates by category.

        Args:
            window: Time window for rate calculation (days)

        Returns:
            DataFrame with inflation rates
        """
        inflation = []

        for category in self.df['category'].unique():
            cat_data = self.df[self.df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()

            # Calculate percentage change
            pct_change = cat_data.pct_change(window) * 100

            inflation.append({
                'category': category,
                'inflation_rate': pct_change.iloc[-1],
                'avg_inflation': pct_change.mean(),
                'inflation_volatility': pct_change.std()
            })

        return pd.DataFrame(inflation)


if __name__ == "__main__":
    # Example usage
    print("TimeSeriesAnalysis module loaded")
