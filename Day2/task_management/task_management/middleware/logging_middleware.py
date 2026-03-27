# middleware/logging_middleware.py
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

import logging
logger = logging.getLogger("api_requests") # Use a separate logger for request logs

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log details of incoming requests and outgoing responses.
    Logs request method, URL, status code, and response time.
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        # Ensure the logger for requests is configured (will be done in main.py)
        # For now, it will use the root logger if not specifically configured.

    async def dispatch(self, request: Request, call_next):
        """
        Dispatches the request through the middleware.
        Logs before and after processing the request.
        """
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        status_code = response.status_code
        
        # Log the request and response details
        log_message = (
            f"Request: {request.method} {request.url.path} "
            f"| Status: {status_code} "
            f"| Time: {process_time:.4f}s"
        )
        
        if status_code >= 500:
            logger.error(log_message)
        elif status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)
            
        return response