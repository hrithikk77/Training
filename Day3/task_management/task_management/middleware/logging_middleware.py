import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logger.info(f"{request.method} {request.url.path} | Status: {response.status_code} | {process_time:.2f}ms")
        return response