from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from decorators.auth import require_role
from models.db_models import Loan
from models.schemas import LoanResponse, LoanReview

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.get("/loans", response_model=list[LoanResponse])
def get_all_loans(
    db: Session = Depends(get_db), 
    current_admin: dict = Depends(require_role("admin"))
):
    """Admin can see every loan in the system."""
    return db.query(Loan).all()

@router.patch("/loans/{loan_id}/review", response_model=LoanResponse)
def review_loan(
    loan_id: int, 
    review: LoanReview, 
    db: Session = Depends(get_db),
    current_admin: dict = Depends(require_role("admin"))
):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    if loan.status != "pending":
        raise HTTPException(status_code=400, detail="Loan already reviewed")
    
    loan.status = review.status
    loan.admin_remarks = review.admin_remarks
    loan.reviewed_by = current_admin["sub"]
    db.commit()
    db.refresh(loan)
    return loan