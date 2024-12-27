from fastapi.testclient import TestClient


async def test_calculate_deposit_endpoint(client: TestClient) -> None:
    """
    Test the /calculate-deposit endpoint with valid input.
    """
    payload = {
        "date": "01.01.2023",
        "periods": 12,
        "amount": 100000,
        "rate": 5.0,
    }
    response = client.post(
        "/api/v1/deposit/calculate-deposit",
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == payload["periods"]
    assert "31.12.2023" in data
    assert data["31.01.2023"] > payload["amount"]


async def test_calculate_deposit_validation_error(client: TestClient) -> None:
    """
    Test the /calculate-deposit endpoint with invalid input.
    """
    payload = {
        "date": "32.13.2023",  # Invalid date
        "periods": 120,  # Out of bounds
        "amount": -5000,  # Negative amount
        "rate": 0.0,  # Invalid rate
    }

    response = client.post(
        "/api/v1/deposit/calculate-deposit",
        json=payload,
    )

    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "date" in data["error"]
    assert "periods" in data["error"]
    assert "amount" in data["error"]
    assert "rate" in data["error"]
