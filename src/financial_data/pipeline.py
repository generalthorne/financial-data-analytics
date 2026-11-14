
from financial_data.ingestion.stock_data import get_stock_data
from financial_data.ingestion.economic_data import get_economic_data

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

