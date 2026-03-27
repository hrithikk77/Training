from fastapi import FastAPI, Depends
from database import engine, Base, SessionLocal, check_db_connection
from models.db_models import User
from models.enums import UserRole
from config import settings
from routers import auth_router, loan_router, admin_router, analytics_router
import logging
from utils.auth_utils import hash_password 

app = FastAPI(title="LoanHub API")


logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app.include_router(auth_router.router)
app.include_router(loan_router.router)
app.include_router(admin_router.router)
app.include_router(analytics_router.router)

@app.on_event("startup")
def startup_event():
    check_db_connection()
    db = SessionLocal()
    
    
    admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    
    if not admin:
        new_admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password=hash_password(settings.ADMIN_PASSWORD), 
            phone="0000000000",
            monthly_income=0,
            role=UserRole.admin
        )
        db.add(new_admin)
        db.commit()
        print("Admin user seeded successfully with hashed password")
    db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}