import pandas as pd
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)
from financial_data.database.operations import save_stock_data
from financial_data.pipeline import analyze_stock


def test_analyze_stock():
    initialize_database()

    dates = pd.bdate_range(
        start="2025-01-06",
        periods=5
    )

    sample_data = pd.DataFrame(
        {
            "Open": [100, 102, 104, 103, 106],
            "High": [103, 105, 106, 107, 109],
            "Low": [99, 101, 102, 102, 104],
            "Close": [100, 102, 104, 103, 106],
            "Volume": [1000000, 1100000, 1200000, 1300000, 1400000],
            "ticker": ["ANALYSIS"] * 5
        },
        index=dates
    )

    save_stock_data(sample_data)

    try:
        results = analyze_stock(
            "ANALYSIS",
            "2025-01-01",
            "2025-01-20"
        )

        assert results["ticker"] == "ANALYSIS"
        assert len(results["daily_returns"]) == 4
        assert len(results["cumulative_returns"]) == 4

        assert results["volatility"] >= 0
        assert results["max_drawdown"] <= 0
        assert isinstance(results["sharpe_ratio"], float)

    finally:
        engine = get_database_engine()

        with engine.begin() as connection:
            connection.execute(
                text("DELETE FROM stock_prices WHERE ticker = 'ANALYSIS'")
            )

        engine.dispose()
