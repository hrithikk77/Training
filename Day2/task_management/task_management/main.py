# main.py
import logging
import os
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware # For enabling CORS

from config import settings
from exceptions.custom_exceptions import (
    UserNotFoundError, DuplicateUserError, InvalidCredentialsError,
    TaskNotFoundError, NotTaskOwnerError, DataIntegrityError
)
from routers import user_router, task_router # Import our routers
from middleware.logging_middleware import LoggingMiddleware # Import our custom middleware

# --- Setup Logging ---
# Ensure the logs directory exists
os.makedirs(os.path.dirname(settings.LOG_FILE_PATH), exist_ok=True)

# Configure the root logger
logger = logging.getLogger() # Get the root logger
logger.setLevel(settings.LOG_LEVEL)

# Define the log format
formatter = logging.Formatter(
    "[%(asctime)s] - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# File handler with rotation
file_handler = RotatingFileHandler(
    settings.LOG_FILE_PATH,
    maxBytes=settings.LOG_FILE_SIZE_MB * 1024 * 1024, # Convert MB to bytes
    backupCount=settings.LOG_BACKUP_COUNT,
    encoding='utf-8'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Optional: Console handler for development if LOG_LEVEL is DEBUG
if settings.LOG_LEVEL.upper() == "DEBUG":
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Get specific loggers for modules that need them, they will inherit config from root
# unless handlers are added specifically to them.
app_logger = logging.getLogger(__name__) # Logger for main.py
app_logger.info("Application starting up...")


# --- FastAPI Application Instance ---
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A simple Task Management API with user authentication and JSON storage.",
    # You can customize OpenAPI docs here
    docs_url="/docs",
    redoc_url="/redoc",
)

# Custom Logging Middleware
app.add_middleware(LoggingMiddleware)

# CORS Middleware (important for frontend applications)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    app_logger.warning(f"Validation error for request: {request.url} | Details: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Validation error",
            "details": exc.errors(),
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

@app.exception_handler(HTTPException) 
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code >= 500:
        app_logger.error(f"HTTP Exception: {exc.detail} | Status: {exc.status_code}", exc_info=True)
    elif exc.status_code >= 400:
        app_logger.warning(f"Client Error: {exc.detail} | Status: {exc.status_code}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__, 
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    app_logger.exception(f"Unhandled exception for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred.",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

#
app.include_router(user_router.router)
app.include_router(task_router.router)


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    app_logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to the {settings.APP_NAME}", "version": settings.APP_VERSION}


@app.on_event("startup")
async def startup_event():
    app_logger.info("FastAPI application startup completed.")
    # Example: Check if JSON files exist and are valid, potentially triggering
    # _ensure_file_exists() from JsonRepository if not already handled.
    # Note: JsonRepository's __init__ already calls _ensure_file_exists via asyncio.run
    #