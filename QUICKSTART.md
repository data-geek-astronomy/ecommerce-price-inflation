# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd ecommerce-price-inflation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Project

### 1. Generate Sample Data
```bash
python src/scraper/main.py
```
This generates 900 sample price records across 5 product categories.

### 2. Run Analysis Pipeline
```bash
python src/analysis/main_analysis.py
```
This performs:
- Time series analysis
- Price trend calculations
- Inflation rate analysis
- Price index construction
- CPI data integration

Output files are saved in `data/processed/`:
- `price_trends.csv` - Trend statistics by category
- `inflation_rates.csv` - Inflation metrics
- `category_indices.csv` - Price indices
- `aggregate_index.csv` - Overall market index
- `cpi_data.csv` - CPI comparison data

### 3. Launch Interactive Dashboard
```bash
streamlit run app/streamlit_app.py
```
This opens an interactive dashboard at `http://localhost:8501`

## Project Structure

```
ecommerce-price-inflation/
├── src/
│   ├── scraper/              # Data collection
│   │   ├── price_scraper.py  # Web scraping module
│   │   └── main.py           # Data collection script
│   ├── analysis/             # Economic analysis
│   │   ├── time_series.py    # Time series methods
│   │   ├── index_builder.py  # Price index construction
│   │   ├── bls_integration.py # CPI data integration
│   │   ├── econometric_models.py # Advanced methods
│   │   └── main_analysis.py  # Analysis pipeline
│   └── utils/                # Utilities
│       ├── config.py         # Configuration
│       └── data_utils.py     # Data processing
├── app/
│   └── streamlit_app.py      # Interactive dashboard
├── data/
│   ├── raw/                  # Raw price data
│   └── processed/            # Analysis results
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
├── METHODOLOGY.md            # Technical methodology
└── QUICKSTART.md            # This file
```

## Dashboard Features

The Streamlit dashboard provides:

- **Overview**: Key metrics and insights
- **Price Trends**: Category price analysis and distribution
- **Inflation Analysis**: Week-over-week inflation rates
- **Indices**: Price index trends over time
- **CPI Comparison**: E-commerce vs traditional retail
- **Data Explorer**: Raw data exploration by category

## Customization

### Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with:
# - BLS_API_KEY (for live CPI data)
# - Data directories
# - Analysis parameters
```

### Modify Analysis Parameters
Edit `src/utils/config.py`:
- `ANALYSIS_LOOKBACK_DAYS`: Historical data window
- `CONFIDENCE_LEVEL`: Statistical significance level
- Category weights for aggregate index

## Sample Commands

### Generate 6 months of data
```python
from src.scraper.price_scraper import PriceScraper
scraper = PriceScraper()
data = scraper.get_sample_data()  # Generates 180 days of data
```

### Analyze specific category
```python
from src.analysis.main_analysis import *
category_data = df_prices[df_prices['category'] == 'Electronics']
```

## Output Interpretation

### Inflation Rate
- Positive: Price increases (deflation is negative)
- Typical range: -50% to +750% for sample data
- Compare across categories to identify hotspots

### Price Index
- Base = 100 at earliest observation
- Values > 100: Prices above base period
- Values < 100: Prices below base period

### Volatility
- Standard deviation of prices
- Higher values = less price stability
- Compare across categories

## Next Steps

1. **Integrate Real Data**: Replace sample data with actual web scraping
2. **Deploy Dashboard**: Push to Streamlit Cloud for public access
3. **Add More Categories**: Expand to 20+ product categories
4. **Implement Predictions**: Add ARIMA/ML models for forecasting
5. **Cross-border Analysis**: Include international e-commerce data

## Troubleshooting

**Port already in use?**
```bash
streamlit run app/streamlit_app.py --server.port 8502
```

**Missing data files?**
```bash
python src/scraper/main.py
python src/analysis/main_analysis.py
```

**Environment variable issues?**
```bash
export BLS_API_KEY="your_key_here"
# or edit .env file
```

## Contact & Resources

- **Email**: rahulreddy12365@gmail.com
- **GitHub**: [Repository URL]
- **Documentation**: See README.md and METHODOLOGY.md
- **BLS API**: https://www.bls.gov/developers/

---

For full technical documentation, see METHODOLOGY.md
