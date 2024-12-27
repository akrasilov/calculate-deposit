from sqlalchemy import inspect

from src.models.deposits import Deposit


def test_deposit_model_columns() -> None:
    """
    Ensure the `Deposit` model has the correct columns with the expected properties.
    """
    inspector = inspect(Deposit)

    columns = {column.key: column for column in inspector.columns}
    assert "date" in columns
    assert "periods" in columns
    assert "amount" in columns
    assert "rate" in columns
    assert "calculation_result" in columns

    assert columns["date"].nullable is False
    assert columns["periods"].nullable is False
    assert columns["amount"].nullable is False
    assert columns["rate"].nullable is False
    assert columns["calculation_result"].nullable is True

    assert str(columns["date"].type) == "DATETIME"
    assert str(columns["periods"].type) == "INTEGER"
    assert str(columns["amount"].type) == "INTEGER"
    assert str(columns["rate"].type) == "FLOAT"
    assert str(columns["calculation_result"].type) == "JSONB"
