from enum import Enum


class DepositConstants(Enum):
    """
    Enumeration for deposit-related constants.

    Attributes:
        MIN_PERIODS (int): Minimum number of deposit months.
        MAX_PERIODS (int): Maximum number of deposit months.

        MIN_AMOUNT (int): Minimum deposit amount.
        MAX_AMOUNT (int): Maximum deposit amount.

        MIN_RATE (float): Minimum interest rate.
        MAX_RATE (float): Maximum interest rate.

        DATE_FORMAT (str): The expected format for deposit dates.
    """

    MIN_PERIODS: int = 1
    MAX_PERIODS: int = 60

    MIN_AMOUNT: int = 10_000
    MAX_AMOUNT: int = 3_000_000

    MIN_RATE: float = 1.0
    MAX_RATE: float = 8.0

    DATE_FORMAT: str = "%d.%m.%Y"
