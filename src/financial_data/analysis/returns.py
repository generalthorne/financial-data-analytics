import pandas as pd


def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    """Calculate daily percentage returns from a price series."""

    returns = prices.pct_change()

    return returns.dropna()


def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
    """Calculate cumulative returns from a series of daily returns."""

    cumulative_returns = (1 + returns).cumprod() - 1

    return cumulative_returns
