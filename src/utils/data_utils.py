"""
Data utility functions.
"""

import pandas as pd
from pathlib import Path
from typing import Optional


def load_price_data(filepath: str) -> pd.DataFrame:
    """
    Load price data from CSV.

    Args:
        filepath: Path to CSV file

    Returns:
        DataFrame with price data
    """
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def prepare_analysis_df(df: pd.DataFrame, min_dates: int = 30) -> pd.DataFrame:
    """
    Prepare data for analysis by filtering and validating.

    Args:
        df: Raw price DataFrame
        min_dates: Minimum number of dates required per category

    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter categories with sufficient data
    category_counts = df.groupby('category')['timestamp'].nunique()
    valid_categories = category_counts[category_counts >= min_dates].index

    df = df[df['category'].isin(valid_categories)]

    # Remove outliers (prices 3 std devs from mean)
    for category in df['category'].unique():
        cat_mask = df['category'] == category
        mean_price = df[cat_mask]['price'].mean()
        std_price = df[cat_mask]['price'].std()

        df = df[
            ~cat_mask | (
                (df['price'] >= mean_price - 3*std_price) &
                (df['price'] <= mean_price + 3*std_price)
            )
        ]

    return df


def create_data_directories():
    """Create necessary data directories."""
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    Path('data/processed').mkdir(parents=True, exist_ok=True)
