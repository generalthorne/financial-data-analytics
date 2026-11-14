
import pandas as pd
import pytest

from financial_data.analysis.portfolio import (
    calculate_portfolio_returns,
    calculate_portfolio_volatility,
    calculate_correlation_matrix
)


def test_calculate_portfolio_returns():
    asset_returns = pd.DataFrame({
        "A": [0.10, 0.05],
        "B": [0.00, 0.10]
    })

    weights = {
        "A": 0.60,
        "B": 0.40
    }

    portfolio_returns = calculate_portfolio_returns(
        asset_returns,
        weights
    )

    assert portfolio_returns.iloc[0] == pytest.approx(0.06)
    assert portfolio_returns.iloc[1] == pytest.approx(0.07)


def test_portfolio_weights_must_sum_to_one():
    asset_returns = pd.DataFrame({
        "A": [0.10, 0.05],
        "B": [0.00, 0.10]
    })

    weights = {
        "A": 0.60,
        "B": 0.30
    }

    with pytest.raises(ValueError):
        calculate_portfolio_returns(asset_returns, weights)


def test_calculate_portfolio_volatility():
    returns = pd.Series([0.01, -0.02, 0.03, -0.01])

    volatility = calculate_portfolio_volatility(returns)

    assert volatility > 0


def test_calculate_correlation_matrix():
    asset_returns = pd.DataFrame({
        "A": [0.01, 0.02, 0.03],
        "B": [0.02, 0.04, 0.06]
    })

    correlation = calculate_correlation_matrix(asset_returns)

    assert correlation.loc["A", "A"] == pytest.approx(1.0)
    assert correlation.loc["B", "B"] == pytest.approx(1.0)
    assert correlation.loc["A", "B"] == pytest.approx(1.0)
