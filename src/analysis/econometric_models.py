"""
Advanced econometric models for causal inference and analysis.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Tuple

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EconometricAnalysis:
    """Advanced econometric methods for price analysis."""

    @staticmethod
    def panel_regression(df: pd.DataFrame, dependent_var: str, independent_vars: list) -> Dict:
        """
        Perform panel regression analysis.

        Args:
            df: DataFrame with panel data
            dependent_var: Dependent variable column name
            independent_vars: List of independent variable column names

        Returns:
            Dictionary with regression results
        """
        try:
            # Prepare formula
            formula = f"{dependent_var} ~ " + " + ".join(independent_vars)

            # Fit OLS model
            model = ols(formula, data=df).fit()

            # Extract results
            results = {
                'r_squared': model.rsquared,
                'adj_r_squared': model.rsquared_adj,
                'f_statistic': model.fvalue,
                'f_pvalue': model.f_pvalue,
                'coefficients': model.params.to_dict(),
                'p_values': model.pvalues.to_dict(),
                'std_errors': model.bse.to_dict(),
                'summary': str(model.summary())
            }

            return results

        except Exception as e:
            logger.error(f"Error in panel regression: {e}")
            return {}

    @staticmethod
    def difference_in_differences(
        df: pd.DataFrame,
        outcome_var: str,
        treatment_var: str,
        time_var: str,
        group_var: str
    ) -> Dict:
        """
        Implement difference-in-differences estimation.

        Args:
            df: DataFrame with treatment and control groups
            outcome_var: Outcome variable
            treatment_var: Binary treatment indicator
            time_var: Time period indicator
            group_var: Group identifier

        Returns:
            Dictionary with DiD results
        """
        try:
            # Create interaction term
            df = df.copy()
            df['treatment_x_time'] = df[treatment_var] * df[time_var]

            # Fit model
            formula = f"{outcome_var} ~ C({group_var}) + C({time_var}) + treatment_x_time"
            model = ols(formula, data=df).fit()

            results = {
                'ate': model.params.get('treatment_x_time', np.nan),
                'ate_pvalue': model.pvalues.get('treatment_x_time', np.nan),
                'ate_se': model.bse.get('treatment_x_time', np.nan),
                'r_squared': model.rsquared,
                'summary': str(model.summary())
            }

            return results

        except Exception as e:
            logger.error(f"Error in DiD analysis: {e}")
            return {}

    @staticmethod
    def calculate_vif(df: pd.DataFrame, independent_vars: list) -> Dict:
        """
        Calculate Variance Inflation Factor for multicollinearity check.

        Args:
            df: DataFrame with variables
            independent_vars: List of independent variable column names

        Returns:
            Dictionary with VIF values
        """
        try:
            vif_data = pd.DataFrame()
            vif_data["Variable"] = independent_vars

            # Calculate VIF
            X = df[independent_vars]
            vif_data["VIF"] = [
                variance_inflation_factor(X.values, i)
                for i in range(X.shape[1])
            ]

            return vif_data.to_dict('records')

        except Exception as e:
            logger.error(f"Error calculating VIF: {e}")
            return {}

    @staticmethod
    def granger_causality_test(df: pd.DataFrame, var1: str, var2: str, lag: int = 4) -> Dict:
        """
        Test for Granger causality between two variables.

        Args:
            df: DataFrame with time series data
            var1: First variable
            var2: Second variable
            lag: Number of lags to test

        Returns:
            Dictionary with test results
        """
        try:
            from statsmodels.tsa.stattools import grangercausalitytests

            df = df.copy()
            df = df[[var1, var2]].dropna()

            results = []

            # Perform test
            gc_result = grangercausalitytests(df, lag, verbose=False)

            for i in range(1, lag + 1):
                test_result = gc_result[i][0]
                results.append({
                    'lag': i,
                    'f_statistic': test_result[0, 0],
                    'p_value': test_result[0, 1],
                    'significant_at_05': test_result[0, 1] < 0.05
                })

            return {
                'causality_tests': results,
                'causes_relationship': f"{var1} -> {var2}"
            }

        except Exception as e:
            logger.error(f"Error in Granger causality test: {e}")
            return {}


if __name__ == "__main__":
    print("Econometric models module loaded")
