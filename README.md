---
title: E-Commerce Price Inflation Dynamics
emoji: 📊
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.28.1
app_file: app/streamlit_app.py
pinned: false
---

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

## 📊 Dashboard Features

**6 Interactive Pages:**
1. **Overview** - Key metrics and insights at a glance
2. **Price Trends** - Category pricing analysis and distribution
3. **Inflation Analysis** - Week-over-week inflation rates
4. **Indices** - Price index trends over time
5. **CPI Comparison** - E-commerce vs traditional retail comparison
6. **Data Explorer** - Raw data inspection by category

## 🛠️ Technical Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy |
| Analysis | Statsmodels, Scikit-learn |
| Visualization | Plotly |
| Backend | Python |
| Deployment | Hugging Face Spaces |

## 📈 Methodology

### Time Series Analysis
- Seasonal decomposition (STL method)
- Stationarity testing (Augmented Dickey-Fuller)
- Moving average and momentum analysis

### Economic Index Construction
- Category-weighted price indices (base = 100)
- Geometric mean aggregation
- Real vs. nominal price tracking

### Inflation Measurement
- Week-over-week percentage changes
- Volatility analysis by category
- Trend extraction and forecasting

## 📊 Data Sources

- **E-commerce prices**: Amazon, Best Buy, Walmart (web scraping)
- **CPI data**: Bureau of Labor Statistics API
- **Economic indicators**: Federal Reserve, Census Bureau

## 🚀 Usage

1. The app automatically generates sample data on first load
2. Navigate through 6 analysis pages using the sidebar
3. Interact with Plotly charts for detailed information
4. Use the Data Explorer to inspect raw prices by category

## 💡 Key Insights

- Tracks inflation across 5+ product categories
- Identifies categories with highest/lowest price changes
- Measures price volatility by category
- Compares e-commerce inflation to CPI
- Provides actionable economic trends

## 📁 Project Structure

```
├── app/
│   └── streamlit_app.py          # Main dashboard application
├── src/
│   ├── scraper/                  # Web scraping modules
│   │   ├── price_scraper.py
│   │   └── main.py
│   ├── analysis/                 # Econometric analysis
│   │   ├── time_series.py
│   │   ├── index_builder.py
│   │   ├── bls_integration.py
│   │   ├── econometric_models.py
│   │   └── main_analysis.py
│   └── utils/                    # Helper functions
│       ├── config.py
│       └── data_utils.py
├── data/
│   ├── raw/                      # Raw scraped price data
│   └── processed/                # Cleaned and analyzed data
├── requirements.txt              # Python dependencies
├── README.md                      # This file
├── METHODOLOGY.md                # Technical methodology
├── QUICKSTART.md                 # Quick start guide
└── LICENSE                       # MIT License
```

## 💻 Local Development

### Prerequisites
- Python 3.9+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/data-geek-astronomy/ecommerce-price-inflation.git
cd ecommerce-price-inflation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Generate sample data
python src/scraper/main.py

# Run analysis
python src/analysis/main_analysis.py

# Launch Streamlit dashboard
streamlit run app/streamlit_app.py
```

Dashboard opens at: `http://localhost:8501`

## 📊 Results & Insights

The analysis reveals:
- E-commerce shows different inflation patterns than CPI
- Online retail tends to be more deflationary than traditional retail
- Competitive pressure in e-commerce moderates price increases
- Electronics and tech more volatile than books and entertainment
- Seasonal patterns differ between online and offline retail

## 🔬 Econometric Methods

### Advanced Techniques
- **Panel Regression** with fixed effects
- **Difference-in-Differences** for causal inference
- **Granger Causality Testing** for lead-lag relationships
- **Stationarity Testing** with Augmented Dickey-Fuller
- **Multicollinearity Detection** using VIF

### Statistical Rigor
- Publication-quality methodology
- Reproducible analysis pipeline
- Clear documentation of assumptions
- Comprehensive error handling

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 📚 Documentation

- **README.md** (this file) - Project overview
- **METHODOLOGY.md** - Detailed econometric methods
- **QUICKSTART.md** - Quick start guide for local development
- **DEPLOYMENT.md** - Deployment instructions
- **HF_DEPLOYMENT.md** - Hugging Face Spaces deployment guide

## 👤 Contact

**Aravind Kumar Nalukurthi**
- Email: aravind.kumar.nalukurthi@gmail.com
- GitHub: [@data-geek-astronomy](https://github.com/data-geek-astronomy)

## 🔗 Links

- **GitHub Repository**: https://github.com/data-geek-astronomy/ecommerce-price-inflation
- **Streamlit Cloud**: https://ecommerce-price-inflation.streamlit.app
- **Hugging Face Spaces**: https://huggingface.co/spaces/Darkweb007/ecommerce-price-inflation

---

**Built for Stripe Economic Insights & Research** 🏦📊
