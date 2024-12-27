from datetime import datetime

from src.schemas.deposits import DepositRequest
from src.utils.deposit import compute_deposit, last_day_of_month, next_month


def test_last_day_of_month() -> None:
    assert last_day_of_month(datetime(2024, 2, 1)) == datetime(2024, 2, 29)
    assert last_day_of_month(datetime(2023, 3, 1)) == datetime(2023, 3, 31)


def test_next_month() -> None:
    assert next_month(datetime(2023, 12, 1)) == datetime(2024, 1, 1)
    assert next_month(datetime(2024, 1, 1)) == datetime(2024, 2, 1)


def test_compute_deposit() -> None:
    payload = DepositRequest(date="01.01.2024", periods=2, amount=10000, rate=5.0)
    result = compute_deposit(payload)

    assert len(result) == 2
    assert result["31.01.2024"] == 10041.67
    assert result["29.02.2024"] == 10083.51
