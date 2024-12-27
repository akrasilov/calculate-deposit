import pytest
from pydantic import ValidationError

from src.schemas.deposits import DepositRequest


def test_valid_deposit_request() -> None:
    payload = {
        "date": "01.01.2024",
        "periods": 12,
        "amount": 10000,
        "rate": 5.0,
    }
    request = DepositRequest(**payload)
    assert request.date.year == 2024


def test_invalid_date_format() -> None:
    payload = {
        "date": "2024-01-01",
        "periods": 12,
        "amount": 10000,
        "rate": 5.0,
    }
    with pytest.raises(ValidationError):
        DepositRequest(**payload)
