
import pandas as pd
import pytest

from financial_data.analysis.risk import (
    calculate_volatility,
    calculate_max_drawdown,
    calculate_sharpe_ratio
)


def test_calculate_volatility():
    returns = pd.Series([0.01, -0.01, 0.02, -0.02])

    volatility = calculate_volatility(
        returns,
        periods_per_year=252
    )

    assert volatility > 0


def test_calculate_max_drawdown():
    returns = pd.Series([0.20, -0.25, 0.10])

    max_drawdown = calculate_max_drawdown(returns)

    assert max_drawdown == pytest.approx(-0.25)


def test_calculate_sharpe_ratio():
    returns = pd.Series([0.01, 0.02, 0.015, 0.025])

    sharpe = calculate_sharpe_ratio(
        returns,
        risk_free_rate=0.0
    )

    assert sharpe > 0


def test_sharpe_ratio_zero_volatility():
    returns = pd.Series([0.01, 0.01, 0.01])

    with pytest.raises(ValueError):
        calculate_sharpe_ratio(returns)
