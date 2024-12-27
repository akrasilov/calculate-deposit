from unittest.mock import AsyncMock, MagicMock

from src.models.deposits import Deposit
from src.services.deposits import DepositService


async def test_get_existing_deposit() -> None:
    mock_session = AsyncMock()

    deposit = Deposit(
        date="2023-01-01",
        periods=12,
        amount=10000,
        rate=5.0,
        calculation_result={"2023-02-01": 10500.0},
    )

    mock_result = MagicMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=deposit)
    mock_session.execute = AsyncMock(return_value=mock_result)

    service = DepositService(session=mock_session)

    result = await service.get(deposit)

    assert result == deposit


async def test_create_deposit() -> None:
    mock_session = AsyncMock()
    service = DepositService(session=mock_session)
    payload = Deposit(date="2024-01-01", periods=12, amount=10000, rate=5.0)
    calculation_result = {"2024-02-01": 10500.0}

    await service.create(payload, calculation_result)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
