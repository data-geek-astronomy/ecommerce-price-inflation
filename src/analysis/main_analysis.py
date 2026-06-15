"""
Main analysis pipeline for e-commerce price inflation.
"""

import logging
import sys
import pandas as pd
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_utils import load_price_data, prepare_analysis_df
from utils.config import load_config
from time_series import TimeSeriesAnalysis
from index_builder import IndexBuilder
from bls_integration import BLSIntegration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_analysis():
    """Execute the full analysis pipeline."""

    config = load_config()
    logger.info("Starting e-commerce price inflation analysis...")

    # Load price data
    logger.info("Loading price data...")
    price_file = Path(config.DATA_RAW_DIR) / "prices_20260615.csv"

    if not price_file.exists():
        logger.error(f"Price data not found at {price_file}")
        return

    df_prices = load_price_data(str(price_file))
    logger.info(f"Loaded {len(df_prices)} price records")

    # Prepare data
    logger.info("Preparing data for analysis...")
    df_clean = prepare_analysis_df(df_prices, min_dates=10)
    logger.info(f"After cleaning: {len(df_clean)} records, {df_clean['category'].nunique()} categories")

    # Time series analysis
    logger.info("Performing time series analysis...")
    ts_analysis = TimeSeriesAnalysis(df_clean)

    trends = ts_analysis.calculate_price_trends(window=30)
    logger.info("\nPrice Trends by Category:")
    print(trends.to_string())

    inflation = ts_analysis.calculate_inflation_rate(window=7)
    logger.info("\nInflation Rates by Category:")
    print(inflation.to_string())

    # Save results
    trends.to_csv(f"{config.DATA_PROCESSED_DIR}/price_trends.csv", index=False)
    inflation.to_csv(f"{config.DATA_PROCESSED_DIR}/inflation_rates.csv", index=False)

    # Build indices
    logger.info("Building price indices...")
    index_builder = IndexBuilder()

    category_indices = index_builder.build_category_indices(df_clean)
    aggregate_index = index_builder.build_aggregate_index(
        category_indices,
        weights={cat: 1/df_clean['category'].nunique() for cat in df_clean['category'].unique()}
    )

    logger.info("\nCategory Indices (Latest):")
    latest_indices = category_indices.sort_values('date').groupby('category').tail(1)
    print(latest_indices.to_string())

    logger.info("\nAggregate Index (Latest 5):")
    print(aggregate_index.sort_values('date').tail(5).to_string())

    # Save indices
    category_indices.to_csv(f"{config.DATA_PROCESSED_DIR}/category_indices.csv", index=False)
    aggregate_index.to_csv(f"{config.DATA_PROCESSED_DIR}/aggregate_index.csv", index=False)

    # Integrate BLS data
    logger.info("Fetching BLS CPI data...")
    bls = BLSIntegration(api_key=config.BLS_API_KEY)
    cpi_data = bls.get_sample_cpi_data()  # Using sample data for demo

    logger.info("CPI Data (Latest):")
    print(cpi_data.sort_values('date').tail(5).to_string())

    cpi_data.to_csv(f"{config.DATA_PROCESSED_DIR}/cpi_data.csv", index=False)

    logger.info("\nAnalysis complete! Results saved to data/processed/")

    return {
        'prices': df_clean,
        'trends': trends,
        'inflation': inflation,
        'category_indices': category_indices,
        'aggregate_index': aggregate_index,
        'cpi_data': cpi_data
    }


if __name__ == "__main__":
    results = run_analysis()
