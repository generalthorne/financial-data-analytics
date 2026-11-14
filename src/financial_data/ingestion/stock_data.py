
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
