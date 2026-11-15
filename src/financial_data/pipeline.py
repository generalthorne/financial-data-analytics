
from financial_data.ingestion.stock_data import get_stock_data
from financial_data.ingestion.economic_data import get_economic_data
import pandas as pd

from financial_data.processing.cleaning import (
    clean_stock_data,
    clean_economic_data
)

from financial_data.database.operations import (
    save_stock_data,
    save_economic_data
)

from financial_data.database.operations import (
    load_stock_data,
    load_economic_data
)

from financial_data.analysis.returns import (
    calculate_daily_returns,
    calculate_cumulative_returns
)

from financial_data.analysis.risk import (
    calculate_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio
)

from financial_data.analysis.portfolio import (
    calculate_portfolio_returns,
    calculate_portfolio_volatility,
    calculate_correlation_matrix
)

def update_stock_data(
    ticker: str,
    start_date: str,
    end_date: str
) -> None:
    """Retrieve, clean, and save historical stock data."""

    data = get_stock_data(ticker, start_date, end_date)

    cleaned_data = clean_stock_data(data)

    save_stock_data(cleaned_data)


def update_economic_data(
    series_id: str,
    start_date: str,
    end_date: str
) -> None:
    """Retrieve, clean, and save economic data."""

    data = get_economic_data(series_id, start_date, end_date)

    cleaned_data = clean_economic_data(data)

    save_economic_data(cleaned_data)


def analyze_stock(
    ticker: str,
    start_date: str,
    end_date: str
) -> dict:
    """Retrieve stored stock data and calculate financial metrics."""

    stock_data = load_stock_data(
        ticker,
        start_date,
        end_date
    )

    daily_returns = calculate_daily_returns(
        stock_data["Close"]
    )

    cumulative_returns = calculate_cumulative_returns(
        daily_returns
    )

    volatility = calculate_volatility(daily_returns)

    max_drawdown = calculate_max_drawdown(daily_returns)

    sharpe_ratio = calculate_sharpe_ratio(daily_returns)

    return {
        "ticker": ticker.upper(),
        "daily_returns": daily_returns,
        "cumulative_returns": cumulative_returns,
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe_ratio
    }




def analyze_portfolio(
    weights: dict[str, float],
    start_date: str,
    end_date: str
) -> dict:
    """Analyze a portfolio of assets using historical market data."""

    asset_returns = {}

    # Retrieve historical data and calculate returns for each asset.
    for ticker in weights:
        stock_data = load_stock_data(
            ticker,
            start_date,
            end_date
        )

        daily_returns = calculate_daily_returns(
            stock_data["Close"]
        )

        asset_returns[ticker] = daily_returns

    # Combine individual asset returns into a DataFrame.
    returns_df = pd.DataFrame(asset_returns)

    # Calculate portfolio returns using the supplied weights.
    portfolio_returns = calculate_portfolio_returns(
        returns_df,
        weights
    )

    # Calculate portfolio risk metrics.
    volatility = calculate_portfolio_volatility(
        portfolio_returns
    )

    max_drawdown = calculate_max_drawdown(
        portfolio_returns
    )

    sharpe_ratio = calculate_sharpe_ratio(
        portfolio_returns
    )

    # Calculate correlations between individual assets.
    correlation_matrix = calculate_correlation_matrix(
        returns_df
    )

    return {
        "weights": weights,
        "asset_returns": returns_df,
        "portfolio_returns": portfolio_returns,
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe_ratio": sharpe_ratio,
        "correlation_matrix": correlation_matrix
    }


    
def compare_portfolio_to_benchmark(
    portfolio_returns: pd.Series,
    benchmark_ticker: str,
    start_date: str,
    end_date: str
) -> dict:
    """Compare portfolio performance against a market benchmark."""

    # Retrieve historical benchmark prices from the database.
    benchmark_data = load_stock_data(
        benchmark_ticker,
        start_date,
        end_date
    )

    # Calculate benchmark daily returns.
    benchmark_returns = calculate_daily_returns(
        benchmark_data["Close"]
    )

    # Align portfolio and benchmark returns by date.
    comparison = pd.concat(
        [
            portfolio_returns.rename("portfolio"),
            benchmark_returns.rename("benchmark")
        ],
        axis=1
    ).dropna()

    if comparison.empty:
        raise ValueError(
            "No overlapping dates between portfolio and benchmark data."
        )

    # Calculate cumulative returns for both.
    portfolio_cumulative = calculate_cumulative_returns(
        comparison["portfolio"]
    )

    benchmark_cumulative = calculate_cumulative_returns(
        comparison["benchmark"]
    )

    # Calculate the difference in cumulative performance.
    excess_returns = portfolio_cumulative - benchmark_cumulative

    # Calculate maximum drawdowns.
    portfolio_max_drawdown = calculate_max_drawdown(
        comparison["portfolio"]
    )

    benchmark_max_drawdown = calculate_max_drawdown(
        comparison["benchmark"]
    )

    return {
        "benchmark_ticker": benchmark_ticker,
        "daily_returns": comparison,
        "portfolio_cumulative_returns": portfolio_cumulative,
        "benchmark_cumulative_returns": benchmark_cumulative,
        "excess_returns": excess_returns,
        "portfolio_max_drawdown": portfolio_max_drawdown,
        "benchmark_max_drawdown": benchmark_max_drawdown
    }


