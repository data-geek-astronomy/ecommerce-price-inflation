"""
Economic index construction module.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IndexBuilder:
    """Constructs price indices from scraped data."""

    def __init__(self, base_date: str = None):
        """
        Initialize index builder.

        Args:
            base_date: Base date for index (format: YYYY-MM-DD)
        """
        self.base_date = base_date
        self.indices = {}

    def build_category_indices(self, df: pd.DataFrame, base_year: int = None) -> pd.DataFrame:
        """
        Build price indices for each category (base = 100).

        Args:
            df: DataFrame with timestamp, category, and price columns
            base_year: Year to use as base period

        Returns:
            DataFrame with index values
        """
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        if base_year is None:
            base_year = df['timestamp'].dt.year.min()

        indices = []

        for category in df['category'].unique():
            cat_data = df[df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()

            # Calculate base price (average for base year)
            base_price = cat_data[cat_data.index.year == base_year].mean()

            if pd.isna(base_price) or base_price == 0:
                logger.warning(f"Invalid base price for {category}, using overall average")
                base_price = cat_data.mean()

            # Calculate index (base = 100)
            index_values = (cat_data / base_price) * 100

            for date, value in index_values.items():
                indices.append({
                    'date': date,
                    'category': category,
                    'index': round(value, 2),
                    'base_year': base_year
                })

        result_df = pd.DataFrame(indices)
        self.indices['category'] = result_df

        return result_df

    def build_aggregate_index(self, df: pd.DataFrame, weights: Dict[str, float] = None) -> pd.DataFrame:
        """
        Build aggregate price index across categories.

        Args:
            df: DataFrame with indices
            weights: Dictionary of category weights (sum should equal 1)

        Returns:
            DataFrame with aggregate index
        """
        if weights is None:
            # Equal weights if not specified
            categories = df['category'].unique()
            weights = {cat: 1/len(categories) for cat in categories}

        # Validate weights
        total_weight = sum(weights.values())
        if not np.isclose(total_weight, 1.0):
            logger.warning(f"Weights sum to {total_weight}, normalizing...")
            weights = {cat: w/total_weight for cat, w in weights.items()}

        aggregate = []

        for date in df['date'].unique():
            date_data = df[df['date'] == date]
            weighted_index = 0

            for _, row in date_data.iterrows():
                category = row['category']
                if category in weights:
                    weighted_index += row['index'] * weights[category]

            aggregate.append({
                'date': date,
                'aggregate_index': round(weighted_index, 2),
                'type': 'Weighted Aggregate'
            })

        result_df = pd.DataFrame(aggregate)
        self.indices['aggregate'] = result_df

        return result_df

    def calculate_index_momentum(self, index_df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
        """
        Calculate momentum of indices.

        Args:
            index_df: DataFrame with index values
            window: Window for momentum calculation

        Returns:
            DataFrame with momentum metrics
        """
        index_df = index_df.copy()
        index_df = index_df.sort_values('date')

        momentum_data = []

        for category in index_df['category'].unique() if 'category' in index_df.columns else ['aggregate']:
            if 'category' in index_df.columns:
                cat_index = index_df[index_df['category'] == category].sort_values('date')
                col = 'index'
            else:
                cat_index = index_df.sort_values('date')
                col = 'aggregate_index'

            if len(cat_index) < window:
                continue

            # Calculate momentum (% change over period)
            momentum = cat_index[col].pct_change(window) * 100

            momentum_data.append({
                'category': category if 'category' in index_df.columns else 'Aggregate',
                'current_momentum': momentum.iloc[-1],
                'avg_momentum': momentum.mean(),
                'momentum_volatility': momentum.std()
            })

        return pd.DataFrame(momentum_data)


if __name__ == "__main__":
    print("IndexBuilder module loaded")
