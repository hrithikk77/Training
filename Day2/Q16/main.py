from fastapi import FastAPI
from config import settings


app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def startup_event():
    print(
        f"App: {settings.APP_NAME} | "
        f"Debug: {settings.DEBUG} | "
        f"DB: {settings.JSON_DB_PATH}"
    )