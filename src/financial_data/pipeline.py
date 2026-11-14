
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
