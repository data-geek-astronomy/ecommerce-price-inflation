# Methodology: E-Commerce Price Inflation Analysis

## Overview

This project applies rigorous econometric methods to analyze price dynamics in e-commerce, comparing online retail pricing to traditional CPI inflation. The analysis is built on economic theory and statistical best practices.

## Data Sources

### Primary Sources
- **E-commerce prices**: Real-time price data from major retailers (Amazon, Best Buy, Walmart)
- **CPI Data**: Bureau of Labor Statistics (BLS) Consumer Price Index
- **Economic Indicators**: Federal Reserve, Census Bureau

### Data Collection
- Daily price sampling across 5+ product categories
- 180-day historical analysis with forward-looking projections
- Stratified sampling across price points and products

## Analytical Methods

### 1. Time Series Analysis

#### Seasonal Decomposition (STL)
- Separates trend, seasonal, and residual components
- Period: 30 days for capturing weekly patterns
- Helps identify structural breaks in pricing

#### Stationarity Testing
- Augmented Dickey-Fuller (ADF) test
- Determines if differencing is needed for modeling
- Critical for ARIMA and VAR modeling

### 2. Price Index Construction

#### Category Indices (Base = 100)
```
Index_t = (Price_t / Base_Price) × 100
```

**Base Period**: 2025 (earliest available data)
**Aggregation Method**: Equal-weighted geometric mean across products

#### Aggregate Index
```
Aggregate_Index = Σ(Category_Index × Weight)
```

**Weights**: Equal-weighted by default, customizable by category

### 3. Inflation Rate Calculation

**Week-over-week percentage change**:
```
Inflation_Rate = (Price_t - Price_t-7) / Price_t-7 × 100%
```

**Metrics**:
- Current inflation rate
- Average inflation (7-day moving average)
- Inflation volatility (standard deviation)

### 4. Causal Inference

#### Difference-in-Differences (DiD)
- Estimates treatment effects of supply shocks
- Compares treated vs. control categories
- Formula:
```
ATE = (Outcome_Treated_Post - Outcome_Treated_Pre) 
      - (Outcome_Control_Post - Outcome_Control_Pre)
```

#### Granger Causality Testing
- Tests whether past values of one variable predict another
- Identifies lead-lag relationships
- 4-lag specification for economic cycles

### 5. Econometric Models

#### Panel Regression
```
Price_it = α + β×Shock_it + γ×Category_i + λ×Time_t + ε_it
```

- Fixed effects for category and time
- Robust standard errors
- R² for model fit assessment

#### Multicollinearity Check
- Variance Inflation Factor (VIF)
- Threshold: VIF < 5 for acceptable collinearity
- Identifies redundant variables

## Key Findings Framework

### Economic Significance
- E-commerce shows different inflation patterns than CPI
- Online retail tends to be more deflationary than traditional retail
- Competitive pressure in e-commerce moderates price increases

### Shock Analysis
- Supply chain disruptions have asymmetric impacts across categories
- Electronics and tech more volatile than books and entertainment
- Seasonal patterns differ between online and offline retail

## Data Quality & Validation

### Outlier Detection
- Prices > 3 standard deviations from category mean removed
- Missing data: forward/backward fill with validation
- Minimum 30 observations per category required

### Reproducibility
- All code version controlled
- Seed-based random number generation
- Analysis pipeline fully documented

## Limitations

1. **Data Scope**: Current analysis covers major online retailers only
2. **Time Period**: Limited to available historical data (180 days)
3. **Categories**: 5 major categories, may not represent all e-commerce
4. **Causality**: DiD methods identify correlations; true causal inference requires quasi-experiments

## Future Enhancements

- Real-time price monitoring and alerts
- Expand to 20+ product categories
- Machine learning for price prediction
- Cross-border e-commerce analysis
- Integration with geolocation data

---

*This methodology aligns with academic standards in econometrics and is suitable for policy-relevant research.*
