# E-Commerce Price Inflation Dynamics - Hugging Face Deployment

This project is deployed on Hugging Face Spaces.

## About This Project

Economic analysis of e-commerce price inflation using real-time data from major retailers and CPI data from the Bureau of Labor Statistics.

## Features

- 📊 Real-time price tracking across e-commerce categories
- 📈 Interactive Streamlit dashboard with 6 analysis pages
- 🔍 Time series analysis with seasonal decomposition
- 💹 Price index construction (base = 100)
- 📉 Inflation rate analysis across categories
- 🌍 CPI comparison with traditional retail
- 🎯 Data explorer for raw price inspection

## Technical Stack

- **Backend**: Python, Pandas, Statsmodels, NumPy
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data**: BLS API (CPI), Web scraping (e-commerce prices)

## Dashboard Pages

1. **Overview** - Key metrics and insights
2. **Price Trends** - Category pricing analysis
3. **Inflation Analysis** - Week-over-week inflation rates
4. **Indices** - Price index trends
5. **CPI Comparison** - E-commerce vs traditional retail
6. **Data Explorer** - Raw data inspection by category

## Usage

The app automatically generates sample data on first load. No setup required!

### Local Development

```bash
git clone https://github.com/data-geek-astronomy/ecommerce-price-inflation.git
cd ecommerce-price-inflation

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Generate data
python src/scraper/main.py
python src/analysis/main_analysis.py

# Run dashboard
streamlit run app/streamlit_app.py
```

## Project Structure

```
├── app/
│   └── streamlit_app.py       # Main dashboard
├── src/
│   ├── scraper/               # Data collection
│   ├── analysis/              # Economic analysis
│   └── utils/                 # Utilities
├── data/
│   ├── raw/                   # Price data
│   └── processed/             # Analysis results
└── requirements.txt           # Dependencies
```

## Data Sources

- **E-commerce Prices**: Amazon, Best Buy, Walmart (web scraping)
- **CPI Data**: Bureau of Labor Statistics API
- **Economic Indicators**: Federal Reserve, Census Bureau

## Methodology

### Time Series Analysis
- Seasonal decomposition (STL)
- Stationarity testing (ADF)
- Moving averages and momentum

### Economic Indices
- Category-weighted price indices
- Aggregate market index
- Index momentum calculations

### Inflation Metrics
- Week-over-week percentage changes
- Category volatility analysis
- Trend extraction

## Results Interpretation

**Inflation Rate**: Positive values indicate price increases; negative indicate deflation
**Price Index**: Base = 100; values > 100 mean prices above base period
**Volatility**: Standard deviation of prices within category

## Performance

- Loads sample data: < 1 second
- Renders visualizations: < 2 seconds
- Full dashboard load: < 5 seconds

## Built For

**Stripe Economic Insights & Research Team** - Demonstrating econometric expertise in:
- Causal inference and panel regression
- Economic research methodology
- Real-time data analysis
- Interactive visualization

## Author

**Aravind Kumar Nalukurthi**  
Email: aravind.kumar.nalukurthi@gmail.com  
GitHub: [@data-geek-astronomy](https://github.com/data-geek-astronomy)

## License

MIT License

---

**Live Demo**: https://huggingface.co/spaces/data-geek-astronomy/ecommerce-price-inflation
