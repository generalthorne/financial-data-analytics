
import pandas as pd
import pandas_market_calendars as mcal


def get_market_rangebreaks(
    start_date,
    end_date,
    interval="1d"
):
    """
    Generate Plotly range breaks using the NYSE trading calendar.

    Hides weekends, market holidays, overnight hours,
    and the unused portion of early-close sessions.
    """

    nyse = mcal.get_calendar("NYSE")

    schedule = nyse.schedule(
        start_date=start_date,
        end_date=end_date
    )

    # Identify weekdays when the market is closed.
    all_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D"
    )

    trading_dates = set(
        schedule.index.strftime("%Y-%m-%d")
    )

    holidays = [
        date.strftime("%Y-%m-%d")
        for date in all_dates
        if date.weekday() < 5
        and date.strftime("%Y-%m-%d") not in trading_dates
    ]

    rangebreaks = [
        dict(bounds=["sat", "mon"]),
        dict(
            values=holidays,
            dvalue=24 * 60 * 60 * 1000
        )
    ]

    if interval != "1d":

        # Hide overnight hours outside the regular session.
        rangebreaks.append(
            dict(
                bounds=[16, 9.5],
                pattern="hour"
            )
        )

        # Hide the unused afternoon after early market closes.
        for _, session in schedule.iterrows():

            market_close = session["market_close"].tz_convert(
                "America/New_York"
            )

            regular_close = market_close.normalize() + pd.Timedelta(
                hours=16
            )

            if market_close < regular_close:

                missing_duration = (
                    regular_close - market_close
                ).total_seconds() * 1000

                rangebreaks.append(
                    dict(
                        values=[market_close],
                        dvalue=missing_duration
                    )
                )

    return rangebreaks
