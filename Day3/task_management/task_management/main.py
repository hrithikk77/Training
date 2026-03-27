from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import user_router, task_router
from config import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(user_router.router)
app.include_router(task_router.router)

@app.get("/")
async def root():
    return {"message": "TaskAPI is running"}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # ADD THIS LINE:
    print(f"CRITICAL ERROR: {exc}") 
    import traceback
    traceback.print_exc() # This prints the full red error log
    
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "error": str(exc)}
    )
