from sqlalchemy.orm import Session
from models.db_models import Loan, User
from decorators.timer import timer

class AnalyticsService:
    @staticmethod
    @timer
    def get_summary(db: Session):
        loans = db.query(Loan).all()
        total_users = db.query(User).count()

        if not loans:
            return {"message": "No data available"}

        # Requirement 10: Using List/Dict Comprehensions
        
        all_statuses = [l.status.value for l in loans]
        status_breakdown = {s: all_statuses.count(s) for s in set(all_statuses)}

        all_purposes = [l.purpose.value for l in loans]
        purpose_breakdown = {p: all_purposes.count(p) for p in set(all_purposes)}

        amounts = [l.amount for l in loans]
        avg_amount = sum(amounts) / len(amounts)

        # 4. Total Disbursed (Sum of ONLY approved loans)
        total_disbursed = sum([l.amount for l in loans if l.status == "approved"])

        return {
            "total_users": total_users,
            "total_loans": len(loans),
            "pending_loans": status_breakdown.get("pending", 0),
            "approved_loans": status_breakdown.get("approved", 0),
            "rejected_loans": status_breakdown.get("rejected", 0),
            "total_disbursed_amount": total_disbursed,
            "avg_loan_amount": round(avg_amount, 2),
            "loans_by_purpose": purpose_breakdown
        }