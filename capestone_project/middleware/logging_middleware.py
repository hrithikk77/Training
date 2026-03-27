import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logger to write to the app.log file
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        response = await call_next(request)
        
        # Calculate process time in milliseconds
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}ms"
        
        # Requirement 9 format: 
        # METHOD /PATH | STATUS_CODE | TIME
        log_message = (
            f"{request.method} {request.url.path} | "
            f"{response.status_code} | {formatted_process_time}"
        )
        
        logging.info(log_message)
        
        # Add the time taken to the response headers (useful for debugging)
        response.headers["X-Process-Time"] = formatted_process_time
        
        return response