
import streamlit as st
import pandas as pd
import plotly.express as px



from financial_data.pipeline import (
    analyze_stock,
    update_stock_data,
    analyze_portfolio,
    compare_portfolio_to_benchmark
)

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
        "Benchmark Comparison"
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
            st.error(f"Invalid portfolio configuration: {error}")


elif page == "Benchmark Comparison":

    st.header("Benchmark Comparison")
    st.info("Benchmark comparison will be implemented next.")
