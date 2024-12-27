import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from settings import AppSettings

logger = logging.getLogger(AppSettings().TITLE)


class LogRequestsMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log details about each request, including duration, method, path, and response status.

    Attributes:
        logger: Logger instance to record request details.

    Methods:
        dispatch(request, call_next):
            Processes the request, measures its duration, logs relevant details, and returns the response.
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        request_duration = time.perf_counter() - start_time
        logger.info(
            "Request",
            extra={
                "request": {
                    "duration_ms": f"{request_duration:.6f}",
                    "path": request.url.path,
                    "method": request.method,
                    "response_status": response.status_code,
                }
            },
        )
        return response
