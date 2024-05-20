from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as err:
            self.logger.error(f"[{__name__}] {err}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"success": False, "reason": "Internal Server Error"},
            )
