from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.constants.deposit import DepositConstants


class DepositRequest(BaseModel):
    """Schema for deposit calculation request."""

    date: datetime = Field(description="Date in dd.mm.yyyy format", examples=["01.01.2023"])
    periods: int = Field(
        ge=DepositConstants.MIN_PERIODS.value,
        le=DepositConstants.MAX_PERIODS.value,
        description="Number of deposit months",
    )
    amount: int = Field(
        ge=DepositConstants.MIN_AMOUNT.value,
        le=DepositConstants.MAX_AMOUNT.value,
        description="Deposit amount",
    )
    rate: float = Field(
        ge=DepositConstants.MIN_RATE.value,
        le=DepositConstants.MAX_RATE.value,
        description="Interest rate",
    )

    @field_validator("date", mode="before")
    def parse_date(cls, value: str) -> datetime:  # noqa: N805
        """Convert string to datetime object based on the expected format."""
        try:
            return datetime.strptime(value, DepositConstants.DATE_FORMAT.value)
        except ValueError:
            raise ValueError(f"Invalid date format: {value}. Expected format: dd.mm.yyyy") from None
