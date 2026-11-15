
import pandas as pd
from sqlalchemy import text

from financial_data.database.connection import (
    get_database_engine,
    initialize_database
)
from financial_data.database.operations import save_stock_data
from financial_data.pipeline import analyze_portfolio


def test_analyze_portfolio():
    initialize_database()

    engine = get_database_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                "DELETE FROM stock_prices "
                "WHERE ticker IN ('AAPL', 'MSFT')"
            )
        )

    engine.dispose()

    dates = pd.bdate_range(
        start="2025-01-06",
        periods=5
    )

    sample_prices = {
        "AAPL": [100, 102, 101, 104, 106],
        "MSFT": [200, 201, 203, 202, 208]
    }

    for ticker, prices in sample_prices.items():
        sample_data = pd.DataFrame(
            {
                "Open": prices,
                "High": [price + 2 for price in prices],
                "Low": [price - 2 for price in prices],
                "Close": prices,
                "Volume": [1000000] * 5,
                "ticker": [ticker] * 5
            },
            index=dates
        )

        save_stock_data(sample_data)

    weights = {
        "AAPL": 0.60,
        "MSFT": 0.40
    }

    try:
        results = analyze_portfolio(
            weights,
            "2025-01-01",
            "2025-01-20"
        )

        assert results["weights"] == weights

        assert len(results["portfolio_returns"]) == 4
        assert len(results["asset_returns"]) == 4

        assert list(results["asset_returns"].columns) == [
            "AAPL",
            "MSFT"
        ]

        assert results["volatility"] >= 0
        assert results["max_drawdown"] <= 0
        assert isinstance(results["sharpe_ratio"], float)

        assert results["correlation_matrix"].shape == (2, 2)

    finally:
        engine = get_database_engine()

        with engine.begin() as connection:
            connection.execute(
                text(
                    "DELETE FROM stock_prices "
                    "WHERE ticker IN ('AAPL', 'MSFT')"
                )
            )

        engine.dispose()
