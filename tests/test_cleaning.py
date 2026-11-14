
import pandas as pd

from financial_data.processing.cleaning import clean_stock_data

from financial_data.processing.cleaning import clean_economic_data


def test_clean_stock_data():
    data = pd.DataFrame(
        {
            "Open": [100.0, 101.0, None],
            "High": [105.0, 106.0, 107.0],
            "Low": [99.0, 100.0, 101.0],
            "Close": [103.0, 104.0, 105.0],
            "Volume": [1000, 1200, 1300],
            "ticker": ["MSFT", "MSFT", "MSFT"]
        },
        index=pd.to_datetime(
            ["2024-01-01", "2024-01-02", "2024-01-03"]
        )
    )

    cleaned = clean_stock_data(data)

    assert len(cleaned) == 2
    assert not cleaned[["Open", "High", "Low", "Close", "Volume"]].isna().any().any()
    assert cleaned.index.is_monotonic_increasing
    assert data.isna().any().any()




def test_clean_economic_data():
    data = pd.Series(
        [100.0, None, 120.0, 110.0],
        index=pd.to_datetime(
            ["2024-01-03", "2024-01-04", "2024-01-01", "2024-01-01"]
        ),
        name="GDP"
    )

    cleaned = clean_economic_data(data)

    assert len(cleaned) == 2
    assert cleaned.index.is_monotonic_increasing
    assert not cleaned.isna().any()
    assert cleaned.name == "GDP"
    assert data.isna().any()

