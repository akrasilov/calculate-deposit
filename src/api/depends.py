from asyncio import AbstractEventLoop, get_running_loop
from concurrent.futures import ThreadPoolExecutor
from typing import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.deposits import DepositService


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session from the application's session factory.

    Args:
        request (Request): The current FastAPI request object.

    Yields:
        AsyncSession: The database session for the request context.
    """
    async with request.app.state.async_session_factory() as session:
        yield session


async def get_executor(request: Request) -> ThreadPoolExecutor:
    """
    Provides the thread pool executor configured in the application state.

    Args:
        request (Request): The current FastAPI request object.

    Returns:
        ThreadPoolExecutor: The thread pool executor.
    """
    return request.app.state.executor


async def get_event_loop() -> AbstractEventLoop:
    """
    Provides the currently running asyncio event loop.

    Returns:
        AbstractEventLoop: The current event loop.
    """
    return get_running_loop()


async def get_deposit_service(session: AsyncSession = Depends(get_db_session)) -> DepositService:
    """
    Provides an instance of the DepositService using the provided database session.

    Args:
        session (AsyncSession): The database session dependency.

    Returns:
        DepositService: An instance of the deposit service.
    """
    return DepositService(session=session)
