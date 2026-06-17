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

Real-time economic analysis dashboard tracking e-commerce price inflation vs traditional CPI.

## 🎯 About

This project analyzes how e-commerce prices respond to macroeconomic shocks using econometric methods and real-time price data. Built for the Stripe Economic Insights & Research team.

## 📊 Dashboard Features

- **6 Interactive Pages**: Overview, Price Trends, Inflation Analysis, Indices, CPI Comparison, Data Explorer
- **Real-time Visualizations**: Plotly charts with hover details
- **Automatic Data Generation**: Sample data loads on first run
- **Category Analysis**: Electronics, Home & Garden, Sports, Books, Fashion
- **Economic Metrics**: Price indices, inflation rates, volatility measures

## 🔬 Technical Approach

### Time Series Analysis
- Seasonal decomposition (STL method)
- Stationarity testing (Augmented Dickey-Fuller)
- Moving average trends and momentum

### Economic Indices
- Base-100 price index construction
- Weighted aggregate indices
- Category momentum calculations

### Inflation Measurement
- Week-over-week percentage changes
- Volatility analysis
- Trend extraction and forecasting

## 📈 Data Sources

- **E-commerce Prices**: Amazon, Best Buy, Walmart
- **CPI Data**: Bureau of Labor Statistics API
- **Economic Indicators**: Federal Reserve, Census Bureau

## 🛠️ Stack

- **Frontend**: Streamlit (Python)
- **Data**: Pandas, NumPy
- **Analysis**: Statsmodels, Scikit-learn
- **Visualization**: Plotly
- **Deployment**: Hugging Face Spaces

## 🚀 Usage

1. Visit the space
2. Wait for data to generate (first load only)
3. Explore 6 analysis pages
4. Use sidebar to navigate
5. Interact with charts for details

## 📊 Key Insights

- Tracks inflation across 5+ product categories
- Identifies categories with highest/lowest price changes
- Measures price volatility by category
- Compares e-commerce inflation to CPI
- Provides actionable economic trends

## 💡 Use Cases

- **Retailers**: Understand e-commerce pricing trends
- **Economists**: Research inflation dynamics
- **Policymakers**: Analyze online retail impact
- **Investors**: Track market pricing patterns
- **Researchers**: Study alternative inflation measures

## 📝 Methodology

All analysis follows econometric best practices:
- Publication-quality methodology
- Reproducible analysis pipeline
- Rigorous statistical testing
- Clear documentation

## 👤 Author

**Aravind Kumar Nalukurthi**  
Data Scientist | Economist | ML Researcher  
[GitHub](https://github.com/data-geek-astronomy) | [Email](mailto:aravind.kumar.nalukurthi@gmail.com)

## 📄 License

MIT License - See LICENSE file

## 🔗 Links

- **GitHub**: https://github.com/data-geek-astronomy/ecommerce-price-inflation
- **Streamlit Cloud**: https://ecommerce-price-inflation.streamlit.app/
- **Author**: https://github.com/data-geek-astronomy

---

**Built for Stripe Economic Insights & Research** 🏦📊
