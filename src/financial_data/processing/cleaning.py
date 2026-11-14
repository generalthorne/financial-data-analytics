
import pandas as pd


def clean_stock_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate historical stock market data."""

    cleaned = data.copy()

    # Ensure dates are sorted chronologically.
    cleaned = cleaned.sort_index()

    # Remove duplicate dates.
    cleaned = cleaned[~cleaned.index.duplicated(keep="last")]

    # Remove observations missing essential market information.
    required_columns = ["Open", "High", "Low", "Close", "Volume"]

    cleaned = cleaned.dropna(subset=required_columns)

    # Ensure numerical columns have numeric data types.
    for column in required_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="raise"
        )

    return cleaned




def clean_economic_data(data: pd.Series) -> pd.Series:
    """Clean and validate an economic time series."""

    cleaned = data.copy()

    # Sort observations chronologically.
    cleaned = cleaned.sort_index()

    # Remove duplicate dates.
    cleaned = cleaned[~cleaned.index.duplicated(keep="last")]

    # Remove missing observations.
    cleaned = cleaned.dropna()

    # Ensure observations contain numerical values.
    cleaned = pd.to_numeric(cleaned, errors="raise")

    return cleaned

