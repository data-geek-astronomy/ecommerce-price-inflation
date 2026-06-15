"""
E-Commerce Price Inflation Dynamics - Interactive Dashboard
Built with Streamlit for real-time economic analysis
"""

import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta

# Set page config
st.set_page_config(
    page_title="E-Commerce Price Inflation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def generate_sample_data():
    """Generate sample data if it doesn't exist."""
    import logging
    import sys

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Add src to path
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))

    try:
        from scraper.price_scraper import PriceScraper
        from utils.config import load_config

        config = load_config()

        # Generate price data
        logger.info("Generating sample price data...")
        scraper = PriceScraper(output_dir=config.DATA_RAW_DIR)
        sample_data = scraper.get_sample_data()
        scraper.save_to_csv(sample_data, "prices_20260615.csv")

        # Run analysis
        logger.info("Running analysis pipeline...")
        from analysis.main_analysis import run_analysis
        results = run_analysis()

        logger.info("Data generation complete!")
        return True
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        return False


@st.cache_data
def load_data():
    """Load analysis results from processed data directory."""
    # Try multiple possible paths
    possible_paths = [
        Path(__file__).parent.parent / "data" / "processed",  # Local development
        Path.cwd() / "data" / "processed",                     # Current working directory
        Path.cwd() / "ecommerce-price-inflation" / "data" / "processed",  # Streamlit Cloud
    ]

    base_path = None
    for path in possible_paths:
        if path.exists() and any(path.glob("*.csv")):
            base_path = path
            break

    # If no data found, generate it
    if base_path is None:
        with st.spinner("📊 Generating sample data for first run..."):
            generate_sample_data()

        # Try paths again after generation
        for path in possible_paths:
            if path.exists() and any(path.glob("*.csv")):
                base_path = path
                break

    if base_path is None:
        st.error("❌ Unable to generate or find data.")
        st.info("Please run locally:\n```\npython src/scraper/main.py\npython src/analysis/main_analysis.py\n```")
        return None

    data = {}
    try:
        data['prices'] = pd.read_csv(base_path / "prices_20260615.csv")
        data['trends'] = pd.read_csv(base_path / "price_trends.csv")
        data['inflation'] = pd.read_csv(base_path / "inflation_rates.csv")
        data['category_indices'] = pd.read_csv(base_path / "category_indices.csv")
        data['aggregate_index'] = pd.read_csv(base_path / "aggregate_index.csv")
        data['cpi_data'] = pd.read_csv(base_path / "cpi_data.csv")
    except FileNotFoundError as e:
        st.error(f"Error loading data files: {e}")
        st.info(f"Looking in: {base_path}")
        return None

    # Convert date columns
    data['prices']['timestamp'] = pd.to_datetime(data['prices']['timestamp'])
    data['category_indices']['date'] = pd.to_datetime(data['category_indices']['date'])
    data['aggregate_index']['date'] = pd.to_datetime(data['aggregate_index']['date'])
    data['cpi_data']['date'] = pd.to_datetime(data['cpi_data']['date'])

    return data


def render_header():
    """Render dashboard header."""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 E-Commerce Price Inflation Dynamics")
        st.markdown(
            "Real-time analysis of price trends across e-commerce categories "
            "vs. traditional retail CPI inflation"
        )
    with col2:
        st.info(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")


def render_key_metrics(data):
    """Render key performance metrics."""
    st.subheader("Key Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        avg_inflation = data['inflation']['inflation_rate'].mean()
        st.metric("Avg Inflation Rate", f"{avg_inflation:.2f}%")

    with col2:
        max_inflation = data['inflation']['inflation_rate'].max()
        st.metric("Max Inflation", f"{max_inflation:.2f}%")

    with col3:
        num_categories = data['inflation']['category'].nunique()
        st.metric("Categories Tracked", num_categories)

    with col4:
        price_volatility = data['trends']['price_volatility'].mean()
        st.metric("Avg Price Volatility", f"{price_volatility:.2f}$")

    with col5:
        num_records = len(data['prices'])
        st.metric("Data Points", f"{num_records:,}")


def render_price_trends(data):
    """Render price trend visualizations."""
    st.subheader("Price Trends by Category")

    # Price trends table
    st.write("**Latest Price Statistics**")
    trends_display = data['trends'][['category', 'latest_price', 'avg_price', 'momentum']].copy()
    trends_display['latest_price'] = trends_display['latest_price'].round(2)
    trends_display['avg_price'] = trends_display['avg_price'].round(2)
    trends_display['momentum'] = (trends_display['momentum'] * 100).round(2).astype(str) + '%'
    st.dataframe(trends_display, use_container_width=True)

    # Price distribution chart
    st.write("**Price Distribution by Category**")
    fig = px.box(
        data['prices'],
        x='category',
        y='price',
        color='category',
        title="Price Distribution Across Categories",
        labels={'price': 'Price ($)', 'category': 'Category'}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Average price by category
    st.write("**Average Price by Category**")
    avg_prices = data['prices'].groupby('category')['price'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=avg_prices.values,
        y=avg_prices.index,
        orientation='h',
        labels={'x': 'Average Price ($)', 'y': 'Category'},
        color=avg_prices.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)


def render_inflation_analysis(data):
    """Render inflation rate analysis."""
    st.subheader("Inflation Rate Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Inflation Rates by Category**")
        inflation_display = data['inflation'][['category', 'inflation_rate', 'inflation_volatility']].copy()
        inflation_display['inflation_rate'] = (inflation_display['inflation_rate']).round(2).astype(str) + '%'
        inflation_display['inflation_volatility'] = (inflation_display['inflation_volatility']).round(2)
        st.dataframe(inflation_display, use_container_width=True)

    with col2:
        st.write("**Inflation Rate Distribution**")
        fig = px.bar(
            data['inflation'].sort_values('inflation_rate', ascending=False),
            x='category',
            y='inflation_rate',
            color='inflation_rate',
            labels={'inflation_rate': 'Inflation Rate (%)', 'category': 'Category'},
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_indices(data):
    """Render price index analysis."""
    st.subheader("Price Indices Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Category Price Indices Over Time**")
        fig = px.line(
            data['category_indices'],
            x='date',
            y='index',
            color='category',
            labels={'index': 'Index (Base=100)', 'date': 'Date'},
            title="Category Price Index Trends"
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**Aggregate E-Commerce Index**")
        agg_clean = data['aggregate_index'].dropna(subset=['aggregate_index'])
        fig = px.line(
            agg_clean,
            x='date',
            y='aggregate_index',
            labels={'aggregate_index': 'Index Value', 'date': 'Date'},
            title="Aggregate E-Commerce Price Index"
        )
        fig.update_traces(line_color='#1f77b4')
        st.plotly_chart(fig, use_container_width=True)


def render_cpi_comparison(data):
    """Render CPI vs E-Commerce comparison."""
    st.subheader("E-Commerce vs CPI Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**CPI Trend**")
        fig = px.line(
            data['cpi_data'],
            x='date',
            y='cpi_value',
            labels={'cpi_value': 'CPI Value', 'date': 'Date'},
            title="Consumer Price Index (CPI-U)",
            color_discrete_sequence=['#FF6B6B']
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("**CPI Statistics**")
        cpi_stats = data['cpi_data']['cpi_value'].describe()
        st.write(f"Latest CPI: {data['cpi_data']['cpi_value'].iloc[-1]:.2f}")
        st.write(f"Mean CPI: {cpi_stats['mean']:.2f}")
        st.write(f"CPI Range: {cpi_stats['min']:.2f} - {cpi_stats['max']:.2f}")


def render_data_explorer(data):
    """Render raw data explorer."""
    st.subheader("Data Explorer")

    selected_category = st.selectbox(
        "Select Category",
        data['prices']['category'].unique()
    )

    cat_data = data['prices'][data['prices']['category'] == selected_category].copy()
    cat_data['timestamp'] = pd.to_datetime(cat_data['timestamp'])
    cat_data = cat_data.sort_values('timestamp')

    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Price", f"${cat_data['price'].mean():.2f}")
    with col2:
        st.metric("Min Price", f"${cat_data['price'].min():.2f}")
    with col3:
        st.metric("Max Price", f"${cat_data['price'].max():.2f}")
    with col4:
        st.metric("Std Dev", f"${cat_data['price'].std():.2f}")

    # Price trend chart
    daily_avg = cat_data.groupby(cat_data['timestamp'].dt.date)['price'].mean()
    fig = px.line(
        x=daily_avg.index,
        y=daily_avg.values,
        labels={'x': 'Date', 'y': 'Price ($)'},
        title=f"Daily Average Price - {selected_category}"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Raw data table
    if st.checkbox("Show raw data"):
        st.dataframe(
            cat_data[['timestamp', 'platform', 'product_id', 'price']].head(100),
            use_container_width=True
        )


def render_insights(data):
    """Render key insights and findings."""
    st.subheader("Key Insights")

    insights = []

    # Find highest inflation
    max_infl_idx = data['inflation']['inflation_rate'].idxmax()
    max_infl_cat = data['inflation'].loc[max_infl_idx, 'category']
    max_infl_val = data['inflation'].loc[max_infl_idx, 'inflation_rate']
    insights.append(
        f"🔴 **Highest Inflation**: {max_infl_cat} category shows {max_infl_val:.2f}% inflation rate"
    )

    # Find lowest inflation
    min_infl_idx = data['inflation']['inflation_rate'].idxmin()
    min_infl_cat = data['inflation'].loc[min_infl_idx, 'category']
    min_infl_val = data['inflation'].loc[min_infl_idx, 'inflation_rate']
    insights.append(
        f"🟢 **Lowest Inflation**: {min_infl_cat} category shows {min_infl_val:.2f}% inflation rate"
    )

    # Volatility insight
    max_vol_idx = data['trends']['price_volatility'].idxmax()
    max_vol_cat = data['trends'].loc[max_vol_idx, 'category']
    max_vol = data['trends'].loc[max_vol_idx, 'price_volatility']
    insights.append(
        f"⚡ **Most Volatile**: {max_vol_cat} category with ${max_vol:.2f} volatility"
    )

    for insight in insights:
        st.info(insight)


def main():
    """Main dashboard application."""

    # Load data
    data = load_data()
    if data is None:
        st.error("Failed to load data. Please ensure analysis has been run.")
        return

    # Render dashboard
    render_header()

    # Sidebar navigation
    page = st.sidebar.radio(
        "📈 Navigation",
        ["Overview", "Price Trends", "Inflation Analysis", "Indices", "CPI Comparison", "Data Explorer"]
    )

    if page == "Overview":
        render_key_metrics(data)
        render_insights(data)

    elif page == "Price Trends":
        render_price_trends(data)

    elif page == "Inflation Analysis":
        render_inflation_analysis(data)

    elif page == "Indices":
        render_indices(data)

    elif page == "CPI Comparison":
        render_cpi_comparison(data)

    elif page == "Data Explorer":
        render_data_explorer(data)

    # Footer
    st.divider()
    st.markdown(
        """
        ---
        **E-Commerce Price Inflation Dynamics** | Built for Stripe Economic Insights Team
        *Real-time analysis of online retail pricing trends vs. traditional CPI inflation*
        """
    )


if __name__ == "__main__":
    main()
