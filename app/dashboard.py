
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from financial_data.pipeline import (
    analyze_stock,
    update_stock_data,
    analyze_portfolio,
    compare_portfolio_to_benchmark,
    update_economic_data
)

from financial_data.database.operations import (
    load_economic_data,
    load_stock_data
)

ECONOMIC_INDICATORS = {
    "Economic Growth": {
        "Real GDP": "GDPC1",
        "Nominal GDP": "GDP"
    },
    "Inflation": {
        "Consumer Price Index (CPI)": "CPIAUCSL",
        "Personal Consumption Expenditures (PCE)": "PCEPI"
    },
    "Employment": {
        "Unemployment Rate": "UNRATE",
        "Nonfarm Payrolls": "PAYEMS"
    },
    "Interest Rates": {
        "Federal Funds Rate": "FEDFUNDS",
        "10-Year Treasury Yield": "GS10"
    },
    "Housing": {
        "Housing Starts": "HOUST"
    },
    "Consumer Activity": {
        "Retail Sales": "RSAFS"
    }
}

st.set_page_config(
    page_title="Financial Data Analytics",
    layout="wide"
)


st.title("Financial Data Analytics Platform")

st.write(
    "Analyze historical market data, evaluate portfolio performance, "
    "and compare investments against market benchmarks."
)


st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select an analysis",
    [
        "Stock Analysis",
        "Portfolio Analysis",
        "Benchmark Comparison",
        "Economic Data"
    ]
)


if page == "Stock Analysis":

    st.header("Stock Analysis")

    ticker = st.text_input(
        "Enter stock ticker",
        value="AAPL"
    ).upper().strip()

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=pd.to_datetime("2025-01-01")
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=pd.Timestamp.today()
        )

    if st.button("Download Data and Analyze"):

        try:
            with st.spinner("Downloading and storing stock data..."):
                update_stock_data(
                    ticker,
                    str(start_date),
                    str(end_date)
                )

            with st.spinner("Calculating financial metrics..."):
                results = analyze_stock(
                    ticker,
                    str(start_date),
                    str(end_date)
                )

                stock_data = load_stock_data(
                    ticker.upper(),
                    str(start_date),
                    str(end_date)
                )

                st.subheader("Price Candlestick Chart")

                candlestick = go.Figure(
                    data=[
                        go.Candlestick(
                            x=stock_data.index,
                            open=stock_data["Open"],
                            high=stock_data["High"],
                            low=stock_data["Low"],
                            close=stock_data["Close"],
                            name=ticker.upper()
                        )
                    ]
                )

                candlestick.update_layout(
                    title=f"{ticker.upper()} Price History",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    xaxis_rangeslider_visible=False
                )

                st.plotly_chart(
                    candlestick,
                    use_container_width=True
                )

            st.subheader("Trading Volume")

            volume_chart = px.bar(
                stock_data,
                x=stock_data.index,
                y="Volume",
                labels={
                    "x": "Date",
                    "Volume": "Shares Traded"
                },
                title=f"{ticker.upper()} Trading Volume"
            )

            st.plotly_chart(
                volume_chart,
                use_container_width=True
            )

            st.subheader(f"{ticker} Analysis")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Annualized Volatility",
                f"{results['volatility']:.2%}"
            )

            metric2.metric(
                "Maximum Drawdown",
                f"{results['max_drawdown']:.2%}"
            )

            metric3.metric(
                "Sharpe Ratio",
                f"{results['sharpe_ratio']:.2f}"
            )

            st.subheader("Cumulative Returns")

            st.line_chart(results["cumulative_returns"])

            st.subheader("Daily Returns")

            st.line_chart(results["daily_returns"])

            st.subheader("30-Day Rolling Volatility")

            rolling_volatility = results["rolling_volatility"]

            fig = px.line(
                rolling_volatility,
                x=rolling_volatility.index,
                y=rolling_volatility.values,
                labels={
                    "x": "Date",
                    "y": "Annualized Volatility"
                },
                title="30-Day Rolling Annualized Volatility"
            )

            fig.update_layout(
                yaxis_tickformat=".1%"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as error:
            st.error(f"Analysis failed: {error}")

        


elif page == "Portfolio Analysis":

    st.header("Portfolio Analysis")

    st.write(
        "Evaluate portfolio performance, measure risk, "
        "and examine relationships between assets."
    )

    st.subheader("Portfolio Configuration")

    tickers_input = st.text_input(
        "Enter stock tickers (comma-separated)",
        value="AAPL, MSFT"
    )

    weights_input = st.text_input(
        "Enter portfolio weights (comma-separated)",
        value="0.60, 0.40"
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=pd.to_datetime("2025-01-01"),
            key="portfolio_start_date"
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=pd.Timestamp.today(),
            key="portfolio_end_date"
        )

    if st.button("Analyze Portfolio"):

        try:
            tickers = [
                ticker.strip().upper()
                for ticker in tickers_input.split(",")
                if ticker.strip()
            ]

            weights = [
                float(weight.strip())
                for weight in weights_input.split(",")
            ]

            if len(tickers) != len(weights):
                raise ValueError(
                    "You must provide exactly one weight for each ticker."
                )

            if len(set(tickers)) != len(tickers):
                raise ValueError(
                    "Duplicate stock tickers are not allowed."
                )

            portfolio_weights = dict(zip(tickers, weights))

            if not abs(sum(weights) - 1.0) < 1e-9:
                raise ValueError(
                    "Portfolio weights must sum to 1.0 (100%)."
                )

            with st.spinner("Downloading and storing portfolio data..."):

                for ticker in tickers:
                    update_stock_data(
                        ticker,
                        str(start_date),
                        str(end_date)
                    )

            with st.spinner("Calculating portfolio metrics..."):
                results = analyze_portfolio(
                    portfolio_weights,
                    str(start_date),
                    str(end_date)
                )

            st.subheader("Portfolio Performance")

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric(
                "Annualized Volatility",
                f"{results['volatility']:.2%}"
            )

            metric2.metric(
                "Maximum Drawdown",
                f"{results['max_drawdown']:.2%}"
            )

            metric3.metric(
                "Sharpe Ratio",
                f"{results['sharpe_ratio']:.2f}"
            )

            st.subheader("Individual Asset Risk Metrics")

            asset_metrics = results["asset_metrics"]

            for ticker, metrics in asset_metrics.items():

                st.write(f"### {ticker}")

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Annualized Volatility",
                    f"{metrics['volatility']:.2%}"
                )

                col2.metric(
                    "Maximum Drawdown",
                    f"{metrics['max_drawdown']:.2%}"
                )

                col3.metric(
                    "Sharpe Ratio",
                    f"{metrics['sharpe_ratio']:.2f}"
                )

            st.subheader("Portfolio Cumulative Returns")

            cumulative_returns = (
                (1 + results["portfolio_returns"]).cumprod() - 1
            )

            st.line_chart(cumulative_returns)

            st.subheader("Portfolio Daily Returns")

            st.line_chart(results["portfolio_returns"])

            correlation_matrix = results["correlation_matrix"]

            fig = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                color_continuous_scale="RdBu",
                zmin=-1,
                zmax=1,
                aspect="auto",
                labels={
                    "color": "Correlation",
                    "x": "Asset",
                    "y": "Asset"
                }
            )

            fig.update_layout(
                xaxis_title="Asset",
                yaxis_title="Asset"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


            st.subheader("Individual Asset Performance")

            asset_cumulative_returns = (
                (1 + results["asset_returns"]).cumprod() - 1
            )

            fig = px.line(
                asset_cumulative_returns,
                x=asset_cumulative_returns.index,
                y=asset_cumulative_returns.columns,
                labels={
                    "x": "Date",
                    "value": "Cumulative Return",
                    "variable": "Asset"
                },
                title="Cumulative Returns by Asset"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as error:
            st.exception(error)


elif page == "Benchmark Comparison":

    st.header("Benchmark Comparison")

    st.write(
        "Compare your portfolio's historical performance "
        "against a market benchmark."
    )

    tickers_input = st.text_input(
        "Portfolio Tickers (comma-separated)",
        value="AAPL, MSFT",
        key="benchmark_tickers"
    )

    weights_input = st.text_input(
        "Portfolio Weights (comma-separated)",
        value="0.60, 0.40",
        key="benchmark_weights"
    )

    benchmark_ticker = st.text_input(
        "Benchmark Ticker",
        value="^GSPC",
        key="benchmark_ticker"
    )

    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime("2020-01-01"),
        key="benchmark_start_date"
    )

    end_date = st.date_input(
        "End Date",
        value=pd.Timestamp.today(),
        key="benchmark_end_date"
    )

    if st.button("Compare Against Benchmark"):

        try:
            tickers = [
                ticker.strip().upper()
                for ticker in tickers_input.split(",")
            ]

            weights = [
                float(weight.strip())
                for weight in weights_input.split(",")
            ]

            if len(tickers) != len(weights):
                raise ValueError(
                    "The number of tickers must match the number of weights."
                )

            if len(set(tickers)) != len(tickers):
                raise ValueError("Duplicate tickers are not allowed.")

            if not tickers or any(not ticker for ticker in tickers):
                raise ValueError("Please enter valid ticker symbols.")

            if not benchmark_ticker.strip():
                raise ValueError("Please enter a benchmark ticker.")

            if not weights or any(weight < 0 or weight > 1 for weight in weights):
                raise ValueError("Weights must be between 0 and 1.")

            if not abs(sum(weights) - 1.0) < 1e-9:
                raise ValueError("Portfolio weights must sum to 1.")

            if start_date >= end_date:
                raise ValueError("Start date must be before end date.")

            portfolio_weights = dict(zip(tickers, weights))

            with st.spinner("Downloading portfolio and benchmark data..."):

                for ticker in tickers:
                    update_stock_data(
                        ticker,
                        str(start_date),
                        str(end_date)
                    )

                update_stock_data(
                    benchmark_ticker.strip().upper(),
                    str(start_date),
                    str(end_date)
                )

                portfolio_results = analyze_portfolio(
                    portfolio_weights,
                    str(start_date),
                    str(end_date)
                )

                comparison_results = compare_portfolio_to_benchmark(
                    portfolio_results["portfolio_returns"],
                    benchmark_ticker.strip().upper(),
                    str(start_date),
                    str(end_date)
                )

            st.success("Benchmark comparison completed!")

            st.subheader("Portfolio vs Benchmark")

            col1, col2 = st.columns(2)

            col1.metric(
                "Portfolio Maximum Drawdown",
                f"{comparison_results['portfolio_max_drawdown']:.2%}"
            )

            col2.metric(
                "Benchmark Maximum Drawdown",
                f"{comparison_results['benchmark_max_drawdown']:.2%}"
            )

            st.subheader("Cumulative Performance")

            performance_data = pd.DataFrame({
                "Portfolio": comparison_results["portfolio_cumulative_returns"],
                "Benchmark": comparison_results["benchmark_cumulative_returns"]
            })

            fig = px.line(
                performance_data,
                x=performance_data.index,
                y=["Portfolio", "Benchmark"],
                labels={
                    "x": "Date",
                    "value": "Cumulative Return",
                    "variable": "Investment"
                },
                title="Portfolio vs Benchmark Returns"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Excess Returns")

            fig = px.line(
                comparison_results["excess_returns"],
                labels={
                    "index": "Date",
                    "value": "Excess Return"
                },
                title="Portfolio Performance Relative to Benchmark"
            )

            fig.update_layout(
                yaxis_title="Excess Return"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.subheader("Daily Return Comparison")

            fig = px.line(
                comparison_results["daily_returns"],
                labels={
                    "index": "Date",
                    "value": "Daily Return",
                    "variable": "Investment"
                },
                title="Daily Portfolio vs Benchmark Returns"
            )

            fig.update_layout(
                yaxis_title="Daily Return"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except ValueError as error:
            st.error(f"Invalid input: {error}")

elif page == "Economic Data":

    st.header("Economic Data Analysis")

    st.write(
        "Retrieve and visualize historical economic indicators "
        "using data from the Federal Reserve Economic Database (FRED)."
    )

    recommended_indicators = {
        name: series_id
        for category in ECONOMIC_INDICATORS.values()
        for name, series_id in category.items()
    }

    indicator_choice = st.selectbox(
        "Search Recommended Economic Indicators",
        options=list(recommended_indicators.keys()),
        index=0
    )

    custom_series_id = st.text_input(
        "Or Enter a Custom FRED Series ID",
        placeholder="Example: DGS2"
    )

    if custom_series_id.strip():
        series_id = custom_series_id.strip().upper()
    else:
        series_id = recommended_indicators[indicator_choice]

    st.write(f"Selected FRED Series ID: `{series_id}`")

    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime("2015-01-01"),
        key="economic_start_date"
    )

    end_date = st.date_input(
        "End Date",
        value=pd.Timestamp.today(),
        key="economic_end_date"
    )

    if st.button("Retrieve Economic Data"):

        try:
            if not series_id.strip():
                raise ValueError("Please enter a FRED series ID.")

            if start_date >= end_date:
                raise ValueError("Start date must be before end date.")

            with st.spinner("Retrieving economic data..."):

                update_economic_data(
                    series_id.strip().upper(),
                    str(start_date),
                    str(end_date)
                )

                economic_data = load_economic_data(
                    series_id.strip().upper(),
                    str(start_date),
                    str(end_date)
                )

            st.success(
                f"Successfully retrieved {series_id.upper()} data."
            )
                        
            st.subheader("Historical Economic Data")

            fig = px.line(
                economic_data,
                x=economic_data.index,
                y=economic_data.values,
                labels={
                    "x": "Date",
                    "y": series_id.upper()
                },
                title=f"{series_id.upper()} Historical Data"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as error:
            st.exception(error)

    st.divider()

    st.subheader("Compare Economic Indicators")

    selected_indicators = st.multiselect(
        "Select Indicators to Compare",
        options=list(recommended_indicators.keys()),
        default=[
            "Real GDP",
            "Unemployment Rate",
            "Consumer Price Index (CPI)"
        ]
    )

    if st.button("Compare Indicators"):

        try:
            if len(selected_indicators) < 2:
                raise ValueError(
                    "Please select at least two indicators."
                )

            indicator_data = {}

            with st.spinner("Retrieving economic indicators..."):

                for indicator in selected_indicators:

                    series_id = recommended_indicators[indicator]

                    update_economic_data(
                        series_id,
                        str(start_date),
                        str(end_date)
                    )

                    indicator_data[indicator] = load_economic_data(
                        series_id,
                        str(start_date),
                        str(end_date)
                    )

            comparison_data = pd.concat(
                indicator_data,
                axis=1
            )

            normalized_data = pd.DataFrame(
                index=comparison_data.index
            )

            for indicator in comparison_data.columns:

                series = comparison_data[indicator].dropna()

                if series.empty or series.iloc[0] == 0:
                    raise ValueError(
                        f"Cannot normalize {indicator}."
                    )

                normalized_data[indicator] = (
                    comparison_data[indicator] / series.iloc[0]
                ) * 100

            st.success("Successfully retrieved all indicators.")

            st.subheader("Indexed Economic Indicator Comparison")

            fig = px.line(
                
                normalized_data,
                labels={
                    "value": "Index (First Observation = 100)",
                    "index": "Date",
                    "variable": "Economic Indicator"
                },
                title="Relative Economic Indicator Changes"
            )
            fig.update_traces(
                connectgaps=True
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as error:
            st.exception(error)
