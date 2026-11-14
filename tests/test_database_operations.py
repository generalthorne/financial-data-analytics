
import pandas as pd
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)
from financial_data.database.operations import save_stock_data


def test_save_stock_data():
    initialize_database()

    dates = pd.to_datetime([
        "2025-01-02",
        "2025-01-03"
    ])

    sample_data = pd.DataFrame(
        {
            "Open": [100.0, 102.0],
            "High": [105.0, 106.0],
            "Low": [99.0, 101.0],
            "Close": [103.0, 104.0],
            "Volume": [1000000, 1200000],
            "ticker": ["TEST", "TEST"]
        },
        index=dates
    )

    save_stock_data(sample_data)

    engine = get_database_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT ticker, date, close
                    FROM stock_prices
                    WHERE ticker = 'TEST'
                    ORDER BY date
                """)
            ).fetchall()

        assert len(result) == 2
        assert result[0].ticker == "TEST"
        assert float(result[0].close) == 103.0
        assert float(result[1].close) == 104.0

    finally:
        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM stock_prices WHERE ticker = 'TEST'")
            )

        engine.dispose()

from financial_data.database.operations import save_economic_data

def test_save_economic_data():
    initialize_database()

    dates = pd.to_datetime([
        "2025-01-01",
        "2025-02-01"
    ])

    sample_data = pd.Series(
        [3.5, 3.7],
        index=dates,
        name="TEST_SERIES"
    )

    save_economic_data(sample_data)

    engine = get_database_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT series_id, date, value
                    FROM economic_data
                    WHERE series_id = 'TEST_SERIES'
                    ORDER BY date
                """)
            ).fetchall()

        assert len(result) == 2
        assert result[0].series_id == "TEST_SERIES"
        assert float(result[0].value) == 3.5
        assert float(result[1].value) == 3.7

    finally:
        with engine.begin() as connection:
            connection.execute(
                text("""
                    DELETE FROM economic_data
                    WHERE series_id = 'TEST_SERIES'
                """)
            )

        engine.dispose()

