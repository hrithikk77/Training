from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.schemas import LoanResponse
from database import get_db
from decorators.auth import require_role
from models.db_models import Loan
from models.schemas import LoanCreate

router = APIRouter(prefix="/loans", tags=["User Loans"])

@router.post("/", response_model=LoanResponse)
def apply_for_loan(
    loan_in: LoanCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("user"))
):
    user_id = current_user["id"]
    pending_count = db.query(Loan).filter(Loan.user_id == user_id, Loan.status == "pending").count()
    if pending_count >= 3:
        raise HTTPException(status_code=400, detail="Maximum 3 pending loans allowed")

    new_loan = Loan(
        user_id=user_id,
        **loan_in.model_dump()
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan

@router.get("/my", response_model=list[LoanResponse])
def get_my_loans(db: Session = Depends(get_db), current_user: dict = Depends(require_role("user"))):
    return db.query(Loan).filter(Loan.user_id == current_user["id"]).all()