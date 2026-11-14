
from financial_data.ingestion.stock_data import get_stock_data


def test_stock_data_retrieval():
    data = get_stock_data(
        ticker="MSFT",
        start_date="2020-01-01",
        end_date="2020-02-01"
    )

    assert not data.empty
    assert "Close" in data.columns
    assert "Volume" in data.columns
    assert "ticker" in data.columns
    assert data["ticker"].iloc[0] == "MSFT"
    assert data.index.is_monotonic_increasing
