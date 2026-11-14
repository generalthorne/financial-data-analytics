import numpy as np
import pandas as pd

from financial_data.analysis.risk import calculate_volatility


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: dict[str, float]
) -> pd.Series:
    """Calculate portfolio returns using asset returns and weights."""

    if asset_returns.empty:
        raise ValueError("Asset returns cannot be empty.")

    if set(asset_returns.columns) != set(weights):
        raise ValueError("Weights must match the asset return columns.")

    weight_series = pd.Series(weights, dtype=float)

    if not np.isclose(weight_series.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.")

    # Use dates where all assets have available returns.
    aligned_returns = asset_returns[weight_series.index].dropna()

    if aligned_returns.empty:
        raise ValueError("No dates have complete asset return data.")

    portfolio_returns = aligned_returns.dot(weight_series)

    return portfolio_returns


def calculate_portfolio_volatility(
    portfolio_returns: pd.Series,
    periods_per_year: int = 252
) -> float:
    """Calculate annualized portfolio volatility."""

    return calculate_volatility(
        portfolio_returns,
        periods_per_year
    )


def calculate_correlation_matrix(
    asset_returns: pd.DataFrame
) -> pd.DataFrame:
    """Calculate the correlation matrix between assets."""

    return asset_returns.corr()
