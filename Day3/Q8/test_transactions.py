# from database import SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from transactions import create_user_with_tasks
# from task_management.task_management.models.db_models import User

from Q4.database import SessionLocal
import os



DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,

)



def run():
    SessionLocal = sessionmaker(
    autocommit=False,
    # autocommit=False → don't save changes automatically
    # You must explicitly call session.commit() to save
    # Like writing in a notebook — changes aren't permanent
    # until you say "save" (commit)
    # If something goes wrong, you can rollback() to undo everything

    autoflush=False,
    # autoflush=False → don't automatically send pending changes
    # to the database before each query
    # Gives you more control over when data is sent

    bind=engine,
    # bind=engine → tells the session WHICH engine (database) to use
    # Like telling the shopping cart which store it belongs to
    )

    session = SessionLocal()

    try:
        
        print("--- Case 1: New user ---")
        result = create_user_with_tasks(
            session,
            "dave",
            "dave@mail.com",
            "pass1234",
            ["Setup environment", "Read documentation", "Complete onboarding"]
        )
        print(result)

        #  Case 2: Duplicate username
        print("\n--- Case 2: Duplicate user ---")
        result = create_user_with_tasks(
            session,
            "dave",  # duplicate
            "dave2@mail.com",
            "pass5678",
            ["Task A", "Task B", "Task C"]
        )
        print(result)

        #  Verify rollback worked
        user = session.query(User).filter_by(username="dave").first()
        print(f"\ndave's total tasks: {len(user.tasks)}")

    finally:
        session.close()


if __name__ == "__main__":
    run()