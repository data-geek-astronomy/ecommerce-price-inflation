# E-Commerce Price Inflation Dynamics

A data-driven economic research project analyzing how e-commerce prices respond to macroeconomic shocks and market dynamics. Built for the Stripe Economic Insights & Research team.

## Overview

This project constructs a real-time price index for online retail across product categories and applies econometric methods to understand inflation dynamics in e-commerce versus traditional retail.

### Key Features
- **Real-time price tracking** across Amazon, Best Buy, and other major retailers
- **CPI integration** with public BLS data for comparative analysis
- **Econometric analysis** including time-series modeling and causal inference
- **Interactive dashboard** built with Streamlit for easy exploration
- **Reproducible research** with publication-quality methodology

## Project Structure

```
├── data/
│   ├── raw/              # Raw scraped price data
│   └── processed/        # Cleaned and analyzed data
├── src/
│   ├── scraper/          # Web scraping modules
│   ├── analysis/         # Econometric analysis
│   ├── utils/            # Helper functions
│   └── __init__.py
├── notebooks/            # Exploratory analysis
├── app/
│   └── streamlit_app.py  # Main dashboard
├── tests/                # Unit tests
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── README.md
```

## Installation

### Prerequisites
- Python 3.9+
- Git

### Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/ecommerce-price-inflation.git
cd ecommerce-price-inflation
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
```bash
cp .env.example .env
# Edit .env with your settings
```

## Usage

### Run Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py
```

### Collect Price Data
```bash
python src/scraper/main.py
```

### Run Analysis
```bash
python src/analysis/econometric_analysis.py
```

## Data Sources

- **E-commerce prices**: Amazon, Best Buy (via web scraping)
- **CPI data**: Bureau of Labor Statistics API
- **Economic indicators**: Federal Reserve, Census Bureau

## Methodology

### Time Series Analysis
- Seasonal decomposition (STL)
- ARIMA modeling for forecasting
- Moving average analysis

### Causal Inference
- Difference-in-differences for supply shocks
- Event study methodology
- Panel regression with fixed effects

### Economic Index Construction
- Category-weighted price indices
- Geometric mean aggregation
- Real vs. nominal price tracking

## Results & Insights

(Analysis and findings will be added as project develops)

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details

## Contact

Built by [Your Name]
Email: rahulreddy12365@gmail.com
