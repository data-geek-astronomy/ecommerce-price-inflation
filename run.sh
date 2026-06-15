#!/bin/bash

# E-Commerce Price Inflation Dashboard - Run Script
# This script ensures data is generated before starting the dashboard

set -e

echo "🚀 Starting E-Commerce Price Inflation Analysis..."
echo ""

# Check if data exists
if [ ! -f "data/processed/price_trends.csv" ]; then
    echo "📊 Generating sample data..."
    python src/scraper/main.py
    echo ""

    echo "🔍 Running analysis pipeline..."
    python src/analysis/main_analysis.py
    echo ""
fi

echo "✅ Data ready! Starting Streamlit dashboard..."
echo ""
streamlit run app/streamlit_app.py
