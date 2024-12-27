from unittest.mock import AsyncMock, MagicMock

from src.api.depends import get_deposit_service, get_event_loop, get_executor
from src.services.deposits import DepositService


async def test_get_executor() -> None:
    request_mock = MagicMock()
    request_mock.app.state.executor = "test_executor"

    result = await get_executor(request_mock)
    assert result == "test_executor"


async def test_get_event_loop() -> None:
    loop = await get_event_loop()
    assert loop.is_running()


async def test_get_deposit_service() -> None:
    mock_session = AsyncMock()
    service = await get_deposit_service(mock_session)
    assert isinstance(service, DepositService)
    assert service.session == mock_session
