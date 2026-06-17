"""
E-Commerce Price Inflation Dynamics - Interactive Dashboard
Built with Streamlit for real-time economic analysis
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta
import random

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


def generate_embedded_data():
    """Generate sample data embedded in the app."""
    try:
        categories = ['Electronics', 'Home & Garden', 'Sports', 'Books', 'Fashion']
        platforms = ['Amazon', 'Best Buy', 'Walmart']

        # Generate prices
        prices_data = []
        base_date = datetime.now() - timedelta(days=180)

        np.random.seed(42)

        for day in range(180):
            current_date = base_date + timedelta(days=day)
            for _ in range(5):
                price = np.random.uniform(20, 500)
                prices_data.append({
                    'timestamp': current_date.isoformat(),
                    'platform': np.random.choice(platforms),
                    'product_id': f"PROD_{np.random.randint(1000, 9999)}",
                    'category': np.random.choice(categories),
                    'price': round(float(price), 2),
                    'currency': 'USD'
                })

        prices_df = pd.DataFrame(prices_data)
        prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'])
    except Exception as e:
        st.error(f"Error generating prices: {e}")
        return None

        # Calculate trends
        trends = []
        for category in prices_df['category'].unique():
            cat_data = prices_df[prices_df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()

            sma = cat_data.rolling(window=30).mean()
            ema = cat_data.ewm(span=30).mean()
            momentum = cat_data.pct_change(30, fill_method=None)

            trends.append({
                'category': category,
                'latest_price': float(cat_data.iloc[-1]),
                'ma_30': float(sma.iloc[-1]) if not pd.isna(sma.iloc[-1]) else 0,
                'ema_30': float(ema.iloc[-1]) if not pd.isna(ema.iloc[-1]) else 0,
                'momentum': float(momentum.iloc[-1]) if not pd.isna(momentum.iloc[-1]) else 0,
                'avg_price': float(cat_data.mean()),
                'price_volatility': float(cat_data.std())
            })

        trends_df = pd.DataFrame(trends)

        # Calculate inflation
        inflation = []
        for category in prices_df['category'].unique():
            cat_data = prices_df[prices_df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()
            pct_change = cat_data.pct_change(7, fill_method=None) * 100

            inflation.append({
                'category': category,
                'inflation_rate': float(pct_change.iloc[-1]) if not pd.isna(pct_change.iloc[-1]) else 0,
                'avg_inflation': float(pct_change.mean()),
                'inflation_volatility': float(pct_change.std())
            })

        inflation_df = pd.DataFrame(inflation)

        # Build indices
        indices = []
        base_year = 2025

        for category in prices_df['category'].unique():
            cat_data = prices_df[prices_df['category'] == category].copy()
            cat_data = cat_data.set_index('timestamp').resample('D')['price'].mean()
            base_price = cat_data[cat_data.index.year == base_year].mean()

            if pd.isna(base_price) or base_price == 0:
                base_price = cat_data.mean()

            index_values = (cat_data / base_price) * 100

            for date, value in index_values.items():
                indices.append({
                    'date': date,
                    'category': category,
                    'index': round(float(value), 2),
                    'base_year': base_year
                })

        indices_df = pd.DataFrame(indices)

        # Aggregate index
        aggregate = []
        categories_list = list(indices_df['category'].unique())
        weights = {cat: 1.0/len(categories_list) for cat in categories_list}

        for date in indices_df['date'].unique():
            date_data = indices_df[indices_df['date'] == date]
            weighted_index = 0.0

            for _, row in date_data.iterrows():
                category = row['category']
                if category in weights:
                    weighted_index += float(row['index']) * weights[category]

            aggregate.append({
                'date': date,
                'aggregate_index': round(float(weighted_index), 2),
                'type': 'Weighted Aggregate'
            })

        aggregate_df = pd.DataFrame(aggregate)

        # CPI data
        cpi_dates = pd.date_range(start='2022-01-01', periods=24, freq='MS')
        base_cpi = 290.0
        cpi_noise = np.cumsum(np.random.normal(1, 0.5, len(cpi_dates)))
        cpi_values = base_cpi + cpi_noise

        cpi_df = pd.DataFrame({
            'date': cpi_dates,
            'cpi_value': cpi_values.round(2)
        })

        return {
            'prices': prices_df,
            'trends': trends_df,
            'inflation': inflation_df,
            'category_indices': indices_df,
            'aggregate_index': aggregate_df,
            'cpi_data': cpi_df
        }

    except Exception as e:
        st.error(f"Critical error in data generation: {str(e)}")
        return None


@st.cache_data
def load_data():
    """Load or generate analysis data."""
    # Try to load from files first
    possible_paths = [
        Path(__file__).parent.parent / "data" / "processed",
        Path.cwd() / "data" / "processed",
        Path.cwd() / "ecommerce-price-inflation" / "data" / "processed",
    ]

    for base_path in possible_paths:
        try:
            if base_path.exists() and (base_path / "prices_20260615.csv").exists():
                data = {}
                data['prices'] = pd.read_csv(base_path / "prices_20260615.csv")
                data['trends'] = pd.read_csv(base_path / "price_trends.csv")
                data['inflation'] = pd.read_csv(base_path / "inflation_rates.csv")
                data['category_indices'] = pd.read_csv(base_path / "category_indices.csv")
                data['aggregate_index'] = pd.read_csv(base_path / "aggregate_index.csv")
                data['cpi_data'] = pd.read_csv(base_path / "cpi_data.csv")

                # Convert dates
                data['prices']['timestamp'] = pd.to_datetime(data['prices']['timestamp'])
                data['category_indices']['date'] = pd.to_datetime(data['category_indices']['date'])
                data['aggregate_index']['date'] = pd.to_datetime(data['aggregate_index']['date'])
                data['cpi_data']['date'] = pd.to_datetime(data['cpi_data']['date'])

                return data
        except Exception as e:
            continue

    # If no files found, generate embedded data
    with st.spinner("🔄 Generating sample data..."):
        data = generate_embedded_data()
        if data is not None:
            return data
        else:
            st.error("❌ Failed to generate data. Please check the error above.")
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
