import logging
from typing import Awaitable, Callable

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from settings import AppSettings

logger = logging.getLogger(AppSettings().TITLE)


class LogExceptionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log unhandled exceptions in requests.
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            response = await call_next(request)
            return response
        except HTTPException as http_exc:
            raise http_exc
        except Exception:
            logger.exception(f"Unhandled exception occurred. Path: {request.url.path}, Method: {request.method}")
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})
