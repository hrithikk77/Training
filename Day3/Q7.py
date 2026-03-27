from sqlalchemy import asc, desc
from Q5 import Task, User

def get_tasks_by_status(session, status):
    tasks = session.query(Task).filter_by(status=status).all()
    return tasks or []

def get_tasks_sorted(session, sort_by="created_at", order="asc"):
    column = getattr(Task, sort_by, None)

    if column is None:
        raise ValueError(f"Invalid column: {sort_by}")

    if order.lower() == "desc":
        tasks = session.query(Task).order_by(desc(column)).all()
    else:
        tasks = session.query(Task).order_by(asc(column)).all()

    return tasks or []

def get_tasks_paginated(session, page=1, limit=10):
    if page < 1:
        page = 1
    offset_value = (page - 1) * limit
    tasks = (
        session.query(Task)
        .offset(offset_value)
        .limit(limit)
        .all()
    )
    return tasks or []

def get_user_with_tasks(session, username):
    user = session.query(User).filter_by(username=username).first()
    return user  

from Q4.database import SessionLocal
# from queries import (
#     get_tasks_by_status,
#     get_tasks_sorted,
#     get_tasks_paginated,
#     get_user_with_tasks
# )

def run():
    session = SessionLocal()
    try:
        pending = get_tasks_by_status(session, "pending")
        print(f"Pending tasks: {len(pending)}")
        for t in pending:
            print(f" - {t.title} ({t.owner.username})")

        sorted_tasks = get_tasks_sorted(session, sort_by="created_at", order="desc")
        print(f"\nSorted (newest first): {[t.title for t in sorted_tasks]}")

        page = get_tasks_paginated(session, page=1, limit=2)
        print(f"\nPage 1 (limit 2): {[t.title for t in page]}")
        user = get_user_with_tasks(session, "alice")

        if user:
            print(f"\n{user.username}'s tasks:")
            for t in user.tasks:
                print(f" - {t.title} ({t.status})")
        else:
            print("User not found")

    finally:
        session.close()

if __name__ == "__main__":
    run()