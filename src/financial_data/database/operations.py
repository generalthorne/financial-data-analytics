import pandas as pd
from sqlalchemy import text

from financial_data.database.connection import get_database_engine

def save_stock_data(data: pd.DataFrame) -> None:
    """Save historical stock price data to the PostgreSQL database."""

    if data.empty:
        raise ValueError("Stock data cannot be empty.")

    required_columns = [
        "Open", "High", "Low", "Close", "Volume", "ticker"
    ]

    if not set(required_columns).issubset(data.columns):
        raise ValueError("Stock data is missing required columns.")

    engine = get_database_engine()

    query = text("""
        INSERT INTO stock_prices (
            ticker, date, open, high, low, close, volume
        )
        VALUES (
            :ticker, :date, :open, :high, :low, :close, :volume
        )
        ON CONFLICT (ticker, date) DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
    """)

    records = []

    for date, row in data.iterrows():
        records.append({
            "ticker": row["ticker"],
            "date": date.date(),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": int(row["Volume"])
        })

    with engine.begin() as connection:
        connection.execute(query, records)

    engine.dispose()



def save_economic_data(data: pd.Series) -> None:
    """Save an economic time series to the PostgreSQL database."""

    if data.empty:
        raise ValueError("Economic data cannot be empty.")

    if data.name is None:
        raise ValueError("Economic data must have a series ID as its name.")

    engine = get_database_engine()

    query = text("""
        INSERT INTO economic_data (
            series_id, date, value
        )
        VALUES (
            :series_id, :date, :value
        )
        ON CONFLICT (series_id, date) DO UPDATE SET
            value = EXCLUDED.value;
    """)

    records = []

    for date, value in data.items():
        records.append({
            "series_id": data.name,
            "date": date.date(),
            "value": float(value)
        })

    with engine.begin() as connection:
        connection.execute(query, records)

    engine.dispose()
