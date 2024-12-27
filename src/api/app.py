from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import AppSettings, PostgresSettings
from src.api.middlewares.exception import LogExceptionMiddleware
from src.api.middlewares.logging import LogRequestsMiddleware
from src.api.routers.v1.deposit import router as deposit_router_v1
from src.schemas.exceptions import ValidationError
from src.utils.logging.logger import init_logger


def setup_middlewares(app: FastAPI) -> None:
    """
    Configure middleware for the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance where middleware will be added.
    """
    app.add_middleware(
        LogExceptionMiddleware,
    )
    app.add_middleware(
        LogRequestsMiddleware,
    )


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation exceptions and format error messages for client responses.

    Args:
        request (Request): The incoming HTTP request that caused the validation error.
        exc (RequestValidationError): The exception instance containing validation details.

    Returns:
        JSONResponse: A formatted response with a 400 status code and validation error messages.
    """
    error_message = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
    return JSONResponse(
        status_code=400,
        content={"error": error_message},
    )


def edit_openapi(app: FastAPI) -> None:
    """
    Customize the OpenAPI schema to replace default validation errors.

    Updates the schema to use a custom "ValidationError" model and adjusts
    the response codes and examples for validation errors.

    Args:
        app (FastAPI): The FastAPI application instance with the schema to modify.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = app.openapi()
    schemas = openapi_schema.get("components", {}).get("schemas", {})
    schemas.pop("HTTPValidationError", None)

    openapi_schema["components"]["schemas"]["ValidationError"] = ValidationError.model_json_schema()

    for path in openapi_schema["paths"].values():
        for method in path.values():
            responses = method.get("responses", {})
            if "422" in responses:
                responses["400"] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "example": {"error": "field_name: validation message"},
                            "schema": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                }
                del responses["422"]

    app.openapi_schema = openapi_schema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Define the application's lifespan, initializing and cleaning up resources.

    This function initializes the database engine, session factory, and thread pool
    executor when the application starts, and disposes of them on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Indicates the application lifespan's active state.
    """
    pg_settings = PostgresSettings()
    app.state.engine = create_async_engine(pg_settings.url, echo=True)
    app.state.async_session_factory = sessionmaker(bind=app.state.engine, class_=AsyncSession, expire_on_commit=False)
    app.state.executor = ThreadPoolExecutor()

    yield

    await app.state.engine.dispose()
    app.state.executor.shutdown(wait=True)


def create_app(settings: AppSettings) -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function initializes logging, configures middleware, registers routes, sets
    up exception handlers, and modifies the OpenAPI schema.

    Args:
        settings (AppSettings): Application settings containing configuration values.

    Returns:
        FastAPI: The initialized FastAPI application instance.
    """
    init_logger(settings.TITLE, settings.IS_DEBUG)
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        lifespan=lifespan,
    )
    setup_middlewares(app)
    app.include_router(deposit_router_v1)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    edit_openapi(app)

    return app
