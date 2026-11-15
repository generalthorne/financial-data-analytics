
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)
from financial_data.pipeline import update_stock_data




def test_stock_data_pipeline():
    initialize_database()

    # Retrieve, clean, and save Microsoft stock data.
    update_stock_data(
        ticker="MSFT",
        start_date="2025-01-01",
        end_date="2025-02-01"
    )

    engine = get_database_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM stock_prices
                    WHERE ticker = 'MSFT'
                    AND date >= '2025-01-01'
                    AND date < '2025-02-01'
                """)
            ).scalar()

        assert result > 0

    finally:
        engine.dispose()


from financial_data.pipeline import update_economic_data

def test_economic_data_pipeline():
    initialize_database()

    # Retrieve, clean, and save unemployment data from FRED.
    update_economic_data(
        series_id="UNRATE",
        start_date="2025-01-01",
        end_date="2025-04-01"
    )

    engine = get_database_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM economic_data
                    WHERE series_id = 'UNRATE'
                    AND date >= '2025-01-01'
                    AND date <= '2025-04-01'
                """)
            ).scalar()

        assert result > 0

    finally:
        engine.dispose()
