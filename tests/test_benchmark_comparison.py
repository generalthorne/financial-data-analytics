
import pandas as pd
import pytest
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)
from financial_data.database.operations import save_stock_data
from financial_data.pipeline import compare_portfolio_to_benchmark


def test_compare_portfolio_to_benchmark():
    initialize_database()

    # Remove any existing test benchmark records.
    engine = get_database_engine()

    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM stock_prices WHERE ticker = 'BENCHTEST'")
        )

    engine.dispose()

    dates = pd.bdate_range(
        start="2025-01-06",
        periods=5
    )

    benchmark_prices = [100, 101, 103, 102, 105]

    benchmark_data = pd.DataFrame(
        {
            "Open": benchmark_prices,
            "High": [price + 2 for price in benchmark_prices],
            "Low": [price - 2 for price in benchmark_prices],
            "Close": benchmark_prices,
            "Volume": [1000000] * 5,
            "ticker": ["BENCHTEST"] * 5
        },
        index=dates
    )

    save_stock_data(benchmark_data)

    portfolio_returns = pd.Series(
        [0.03, 0.01, -0.02, 0.04],
        index=dates[1:]
    )

    try:
        results = compare_portfolio_to_benchmark(
            portfolio_returns,
            "BENCHTEST",
            "2025-01-01",
            "2025-01-20"
        )

        assert results["benchmark_ticker"] == "BENCHTEST"

        assert len(results["daily_returns"]) == 4

        assert len(results["portfolio_cumulative_returns"]) == 4
        assert len(results["benchmark_cumulative_returns"]) == 4
        assert len(results["excess_returns"]) == 4

        assert results["portfolio_cumulative_returns"].iloc[-1] == pytest.approx(
            1.03 * 1.01 * 0.98 * 1.04 - 1
        )

        assert results["benchmark_cumulative_returns"].iloc[-1] == pytest.approx(
            1.05 - 1
        )

        assert results["excess_returns"].iloc[-1] == pytest.approx(
            results["portfolio_cumulative_returns"].iloc[-1]
            - results["benchmark_cumulative_returns"].iloc[-1]
        )

        assert results["portfolio_max_drawdown"] <= 0
        assert results["benchmark_max_drawdown"] <= 0

    finally:
        engine = get_database_engine()

        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM stock_prices WHERE ticker = 'BENCHTEST'")
            )

        engine.dispose()
