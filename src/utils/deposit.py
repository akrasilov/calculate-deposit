"""
Utility functions for deposit calculation.

Provides helper functions for calculating the last day of a month, advancing to the next month,
and computing the growth of a deposit over a specified period.
"""

from calendar import monthrange
from datetime import datetime

from src.constants.deposit import DepositConstants
from src.schemas.deposits import DepositRequest


def last_day_of_month(date: datetime) -> datetime:
    """
    Get the last day of the month for a given date.

    Args:
        date (datetime): The date for which to calculate the last day of the month.

    Returns:
        datetime: A datetime object representing the last day of the month.
    """
    last_day = monthrange(date.year, date.month)[1]
    return datetime(date.year, date.month, last_day)


def next_month(date: datetime) -> datetime:
    """
    Get the first day of the next month for a given date.

    Args:
        date (datetime): The date for which to calculate the first day of the next month.

    Returns:
        datetime: A datetime object representing the first day of the next month.
    """
    next_month = (date.month % 12) + 1
    next_year = date.year + (date.month // 12)
    return datetime(next_year, next_month, 1)


def compute_deposit(payload: DepositRequest) -> dict[str, float]:
    """
    Calculate the compound growth of a deposit over time.

    Args:
        payload (DepositRequest): The deposit details, including the start date, periods, amount, and rate.

    Returns:
        dict[str, float]:
            A dictionary where keys are dates (as strings) and values are the deposit values on those dates.
    """
    results = {}
    date = last_day_of_month(payload.date)
    for i in range(1, payload.periods + 1):
        future_value = payload.amount * (1 + payload.rate / 100 / 12) ** i
        results[date.strftime(DepositConstants.DATE_FORMAT.value)] = round(future_value, 2)
        date = last_day_of_month(next_month(date))
    return results
