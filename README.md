# Financial Data Analytics Platform

A Python application for analyzing historical stock market data, portfolios, and economic indicators. The project uses financial data from Yahoo Finance and FRED, stores historical data in PostgreSQL, and presents the results through an interactive Streamlit dashboard.

## Features

### Stock Analysis
- Retrieve historical stock data using Yahoo Finance.
- View interactive candlestick charts and trading volume.
- Analyze daily and cumulative returns.
- Calculate annualized volatility, maximum drawdown, and Sharpe ratio.
- View rolling volatility over time.
- Support multiple candlestick intervals, including 5-minute, 15-minute, 30-minute, 1-hour, and daily intervals.

### Portfolio Analysis
- Analyze portfolios containing multiple stocks.
- Calculate portfolio returns and risk metrics.
- Compare the performance of individual assets.
- View correlation matrices between portfolio assets.

### Benchmark Comparison
- Compare portfolio performance against a market benchmark.
- View cumulative returns for both investments.
- Calculate and visualize excess returns.
- Compare daily returns and maximum drawdowns.

### Economic Data
- Retrieve economic indicators using the FRED API.
- Explore indicators such as GDP, CPI, unemployment, interest rates, and housing starts.
- Compare multiple indicators using percentage changes over time.

## Technologies

- Python
- Pandas
- NumPy
- PostgreSQL
- SQLAlchemy
- yfinance
- FRED API
- Plotly
- Streamlit
- pytest


## Project Structure

The project is organized into the following main directories:

- `src/financial_data/ingestion/` – Retrieves stock market and economic data.
- `src/financial_data/processing/` – Cleans and prepares incoming data.
- `src/financial_data/database/` – Handles PostgreSQL connections and data storage.
- `src/financial_data/analysis/` – Contains return, risk, and portfolio calculations.
- `src/financial_data/market_calendar.py` – Handles market holidays and trading hours.
- `src/financial_data/pipeline.py` – Connects data retrieval, processing, storage, and analysis.
- `app/dashboard.py` – Contains the Streamlit dashboard.
- `tests/` – Contains automated tests.


The code is separated into several components:

- `ingestion`: Retrieves stock market and economic data.
- `processing`: Cleans and prepares incoming data.
- `database`: Handles PostgreSQL connections and data storage.
- `analysis`: Contains return, risk, and portfolio calculations.
- `market_calendar.py`: Handles market holidays and trading hours for financial charts.
- `pipeline.py`: Connects data retrieval, processing, storage, and analysis.
- `app`: Contains the Streamlit dashboard.

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd financial-data-analytics
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

Add the required FRED API key and PostgreSQL connection settings.

### 5. Set