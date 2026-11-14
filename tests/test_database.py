from sqlalchemy import inspect

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)


def test_database_initialization():
    initialize_database()

    engine = get_database_engine()

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "stock_prices" in tables
    assert "economic_data" in tables

    engine.dispose()