import pandas as pd


def calculate_volatility(
    returns: pd.Series,
    periods_per_year: int = 252
) -> float:
    """Calculate annualized volatility from periodic returns."""

    return returns.std() * (periods_per_year ** 0.5)


def calculate_max_drawdown(returns: pd.Series) -> float:
    """Calculate the maximum drawdown from a series of returns."""

    cumulative_returns = (1 + returns).cumprod()

    running_max = cumulative_returns.cummax()

    drawdowns = (cumulative_returns / running_max) - 1

    return drawdowns.min()


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252
) -> float:
    """Calculate the annualized Sharpe ratio."""

    excess_returns = returns - (risk_free_rate / periods_per_year)

    volatility = excess_returns.std()

    if volatility == 0 or pd.isna(volatility):
        raise ValueError("Sharpe ratio cannot be calculated with zero volatility.")

    return (
        excess_returns.mean() / volatility
    ) * (periods_per_year ** 0.5)


def calculate_rolling_volatility(
        returns: pd.Series,
        window: int = 30,
        periods_per_year: int = 252
    ) -> pd.Series:
    """Calculate annualized rolling volatility from periodic returns."""

    rolling_volatility = (
        returns.rolling(window).std()
        * (periods_per_year ** 0.5)
    )

    return rolling_volatility.dropna()