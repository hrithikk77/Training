from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from decorators.auth import require_role
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db), 
    admin: dict = Depends(require_role("admin"))
):
    return AnalyticsService.get_summary(db)