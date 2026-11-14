
import pandas as pd
import pytest

from financial_data.analysis.returns import (
    calculate_daily_returns,
    calculate_cumulative_returns
)


def test_calculate_daily_returns():
    prices = pd.Series([100.0, 105.0, 110.0])

    returns = calculate_daily_returns(prices)

    assert len(returns) == 2
    assert returns.iloc[0] == pytest.approx(0.05)
    assert returns.iloc[1] == pytest.approx(110 / 105 - 1)


def test_calculate_cumulative_returns():
    returns = pd.Series([0.05, 0.10])

    cumulative = calculate_cumulative_returns(returns)

    assert cumulative.iloc[0] == pytest.approx(0.05)
    assert cumulative.iloc[1] == pytest.approx(0.155)
