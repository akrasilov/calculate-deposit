from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.deposits import Deposit


class DepositService:
    """Service for interacting with the deposits table."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, payload: Deposit) -> Deposit | None:
        """
        Retrieve a deposit record by its parameters.

        Args:
            payload (DepositRequest): The request object containing deposit details.

        Returns:
            Deposit | None: The matching deposit record or None if not found.
        """
        result = await self.session.execute(
            select(Deposit).where(
                Deposit.date == payload.date,
                Deposit.periods == payload.periods,
                Deposit.amount == payload.amount,
                Deposit.rate == payload.rate,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, payload: Deposit, calculation_result: dict) -> None:
        """
        Create a new deposit record.

        Args:
            payload (DepositRequest): The request object containing deposit details.
            calculation_result (dict): The result of the deposit calculation.
        """
        deposit = Deposit(
            date=payload.date,
            periods=payload.periods,
            amount=payload.amount,
            rate=payload.rate,
            calculation_result=calculation_result,
        )
        self.session.add(deposit)
        await self.session.commit()
