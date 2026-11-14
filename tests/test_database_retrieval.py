
import pandas as pd
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)

from financial_data.database.operations import (
    save_stock_data,
    save_economic_data,
    load_stock_data,
    load_economic_data
)


def test_load_stock_data():
    initialize_database()

    dates = pd.to_datetime([
        "2025-03-03",
        "2025-03-04"
    ])

    sample_data = pd.DataFrame(
        {
            "Open": [100.0, 102.0],
            "High": [105.0, 106.0],
            "Low": [99.0, 101.0],
            "Close": [103.0, 104.0],
            "Volume": [1000000, 1200000],
            "ticker": ["LOADTEST", "LOADTEST"]
        },
        index=dates
    )

    save_stock_data(sample_data)

    try:
        loaded_data = load_stock_data(
            "LOADTEST",
            "2025-03-01",
            "2025-03-05"
        )

        assert len(loaded_data) == 2
        assert loaded_data["Close"].tolist() == [103.0, 104.0]
        assert loaded_data["ticker"].tolist() == ["LOADTEST", "LOADTEST"]
        assert loaded_data.index.is_monotonic_increasing

    finally:
        engine = get_database_engine()

        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM stock_prices WHERE ticker = 'LOADTEST'")
            )

        engine.dispose()


def test_load_economic_data():
    initialize_database()

    dates = pd.to_datetime([
        "2025-03-01",
        "2025-04-01"
    ])

    sample_data = pd.Series(
        [3.5, 3.7],
        index=dates,
        name="LOADTEST_SERIES"
    )

    save_economic_data(sample_data)

    try:
        loaded_data = load_economic_data(
            "LOADTEST_SERIES",
            "2025-03-01",
            "2025-05-01"
        )

        assert len(loaded_data) == 2
        assert loaded_data.tolist() == [3.5, 3.7]
        assert loaded_data.name == "LOADTEST_SERIES"
        assert loaded_data.index.is_monotonic_increasing

    finally:
        engine = get_database_engine()

        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM economic_data
                    WHERE series_id = 'LOADTEST_SERIES'
                """)
            )

        engine.dispose()
