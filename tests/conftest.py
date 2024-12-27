from typing import AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture()
async def app() -> FastAPI:
    from run_app import app

    return app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[TestClient, None]:
    with TestClient(app=app) as client:
        yield client
