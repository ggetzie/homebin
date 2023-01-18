#! /usr/bin/env python
import argparse
import datetime
from dateutil.relativedelta import relativedelta


def tweets_per_month(start: str, tweets: int) -> int:

    rd = relativedelta(datetime.date.today(), datetime.date.fromisoformat(start))
    total_months = rd.years * 12 + rd.months
    return tweets / total_months


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate tweets per month.")
    parser.add_argument(
        "start_date",
        type=str,
        nargs=1,
        help="The Twitter accounts's start date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "number_of_tweets",
        type=int,
        nargs=1,
        help="The total number of tweets for the account.",
    )
    args = parser.parse_args()
    res = tweets_per_month(args.start_date[0], args.number_of_tweets[0])
    print(f"{res:.2f}")
