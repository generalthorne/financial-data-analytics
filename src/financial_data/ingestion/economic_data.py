import os

import pandas as pd
from dotenv import load_dotenv
from fredapi import Fred


load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")


def get_fred_client() -> Fred:
    """Return an authenticated FRED API client."""

    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY not found in .env file.")

    return Fred(api_key=FRED_API_KEY)


def get_economic_data(
    series_id: str,
    start_date: str,
    end_date: str
) -> pd.Series:
    """Retrieve an economic time series from FRED."""

    fred = get_fred_client()

    data = fred.get_series(
        series_id,
        observation_start=start_date,
        observation_end=end_date
    )

    if data.empty:
        raise ValueError(f"No observations found for series {series_id}.")

    data.name = series_id

    return data