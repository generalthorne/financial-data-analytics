
from financial_data.ingestion.economic_data import (
    get_fred_client,
    get_economic_data
)


def test_fred_connection():
    fred = get_fred_client()

    assert fred is not None


def test_gdp_data_retrieval():
    data = get_economic_data(
        series_id="GDP",
        start_date="2020-01-01",
        end_date="2025-12-31"
    )

    assert not data.empty
    assert data.name == "GDP"
    assert data.index.is_monotonic_increasing
