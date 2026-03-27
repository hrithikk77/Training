from sqlalchemy.orm import Session
from capestone_project.exceptions.custom_exceptions import MaxPendingLoansError
from capestone_project.models.db_models import Loan
from capestone_project.models.schemas import LoanCreate, LoanReview
from capestone_project.exceptions.custom_exceptions import LoanNotFoundError, InvalidLoanReviewError
from decorators.timer import timer
from datetime import datetime

class LoanService:
    @staticmethod
    @timer
    def apply_loan(db: Session, loan_in: LoanCreate, user_id: int):
        # Business Rule: User cannot have more than 3 pending loans
        pending_count = db.query(Loan).filter(
            Loan.user_id == user_id, 
            Loan.status == "pending"
        ).count()
        
        if pending_count >= 3:
            raise MaxPendingLoansError()

        new_loan = Loan(
            user_id=user_id,
            amount=loan_in.amount,
            purpose=loan_in.purpose,
            tenure_months=loan_in.tenure_months,
            employment_status=loan_in.employment_status
        )
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan

    @staticmethod
    @timer
    def review_loan(db: Session, loan_id: int, review_in: LoanReview, admin_username: str):
        loan = db.query(Loan).filter(Loan.id == loan_id).first()
        
        if not loan:
            raise LoanNotFoundError()
        
        # Business Rule: Cannot re-review an already approved/rejected loan
        if loan.status != "pending":
            raise InvalidLoanReviewError("This loan has already been reviewed.")

        # Atomic Transaction (Update all fields at once)
        loan.status = review_in.status
        loan.admin_remarks = review_in.admin_remarks
        loan.reviewed_by = admin_username
        loan.reviewed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(loan)
        return loan
    


    