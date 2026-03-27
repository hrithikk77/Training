

import sys
import os
# This tells Python to look one folder up to find Q5.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Q5 import User, Task # Now it will find it!

# Use the real model file we created for the project
# from models.db_models import User, Task
def create_user_with_tasks(session, username, email, password, task_titles):
    try:
        # 1 Create user
        user = User(
            username=username,
            email=email,
            password=password
        )
        session.add(user)

        # Flush to get user.id (without committing)
        session.flush()

        tasks = []
        for title in task_titles:
            task = Task(
                title=title,
                status="pending",
                owner_id=user.id
            )
            tasks.append(task)

        session.add_all(tasks)

        # 3 Commit (everything saved together)
        session.commit()

        return f"Transaction successful: User '{username}' created with {len(tasks)} tasks"

    except Exception as e:
        #  Rollback EVERYTHING
        session.rollback()

        print(f"Transaction rolled back: {e}")
        print(f"{email} was NOT saved")

        return "Transaction failed"