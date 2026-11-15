
import pandas as pd
import yfinance as yf


def get_stock_data(
    ticker: str,
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """Retrieve historical stock market data."""

    stock = yf.Ticker(ticker)

    data = stock.history(
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    if data.empty:
        raise ValueError(f"No data found for ticker {ticker}.")

    data.index.name = "date"
    data["ticker"] = ticker.upper()

    return data


def get_intraday_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "5m"
) -> pd.DataFrame:
    """Retrieve intraday stock market data."""

    valid_intervals = ["5m", "15m", "30m", "1h"]

    if interval not in valid_intervals:
        raise ValueError(
            f"Interval must be one of {valid_intervals}."
        )

    stock = yf.Ticker(ticker)

    data = stock.history(
        start=start_date,
        end=end_date,
        interval=interval,
        auto_adjust=True
    )

    if data.empty:
        raise ValueError(
            f"No intraday data found for ticker {ticker}."
        )

    data.index.name = "date"
    data["ticker"] = ticker.upper()

    return data