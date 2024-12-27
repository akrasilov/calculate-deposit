from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Depends

from src.api.depends import get_deposit_service, get_event_loop, get_executor
from src.schemas.deposits import DepositRequest
from src.services.deposits import DepositService
from src.utils.deposit import compute_deposit

router = APIRouter(prefix="/api/v1/deposit", tags=["deposit"])


@router.post("/calculate-deposit")
async def calculate_deposit(
    payload: DepositRequest,
    deposit_service: DepositService = Depends(get_deposit_service),
    executor: ThreadPoolExecutor = Depends(get_executor),
    loop: AbstractEventLoop = Depends(get_event_loop),
) -> dict[str, str | float]:
    """
    Calculate or retrieve deposit details.

    This endpoint accepts deposit parameters and calculates the deposit details.
    If the same parameters already exist in the database, it retrieves the existing result.
    Otherwise, it performs the calculation, saves the result to the database, and returns it.

    Args:
        payload (DepositRequest): The deposit parameters.
        deposit_service (DepositService): Dependency for interacting with the database.
        executor (ThreadPoolExecutor): Thread pool for running blocking computations.
        loop (AbstractEventLoop): Current asyncio event loop.

    Returns:
        dict[str, str | float]: The calculation result as a dictionary.
    """
    deposit = await deposit_service.get(payload)
    if deposit:
        return deposit.calculation_result
    calculation_result = await loop.run_in_executor(executor, compute_deposit, payload)
    await deposit_service.create(payload, calculation_result)
    return calculation_result
