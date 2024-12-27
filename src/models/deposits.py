from sqlalchemy import Column, DateTime, Float, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from src.models.core import Base


class Deposit(Base):
    """
    ORM model for the 'deposits' table.

    Represents a deposit record with unique parameters (date, periods, amount, and rate).
    Stores calculation results in a JSONB field.

    Attributes:
        date (DateTime): The date of the deposit.
        periods (Integer): The number of periods for the deposit.
        amount (Integer): The amount deposited.
        rate (Float): The interest rate of the deposit.
        calculation_result (JSONB): The JSONB column to store calculation results.
    """

    __tablename__ = "deposits"

    date = Column(DateTime, nullable=False)
    periods = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    rate = Column(Float, nullable=False)
    calculation_result = Column(JSONB)

    __table_args__ = (UniqueConstraint("date", "periods", "amount", "rate", name="uq_deposit_params"),)
