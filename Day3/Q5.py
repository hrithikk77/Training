# models.py
# ============================================================
# Q5 — SQLAlchemy Models: User and Task
# ============================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# Column     → defines a column in the table
# Integer    → whole numbers (1, 2, 3...)
# String     → short text with max length
# Text       → long text with no length limit
# DateTime   → stores date and time
# ForeignKey → links this column to another table's column

from sqlalchemy.orm import relationship
# relationship() → creates a Python-level link between two models
# Lets you do user.tasks or task.owner without writing SQL JOIN

from datetime import datetime, timezone
# datetime.now(timezone.utc) → current time in UTC
# We use this as the default value for created_at and updated_at

from Q4.database import Base
# Base = declarative_base() from our database.py (Q4)
# Every model MUST inherit from Base
# This is how SQLAlchemy knows "this class = a database table"


# ============================================================
# MODEL 1: User
# ============================================================

class User(Base):
    __tablename__ = "users"
    # Exact name of the table in PostgreSQL database
    # Must match your Day-2 table name exactly

    # ---- COLUMNS ----

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Integer       → stores whole numbers
    # primary_key   → unique identifier for each row
    # autoincrement → database auto-assigns 1, 2, 3...
    # You never set this manually

    username = Column(String(50), unique=True, nullable=False)
    # String(50)  → text up to 50 characters
    # unique=True → no two users can have same username
    # nullable=False → required field, cannot be empty

    email = Column(String(100), unique=True, nullable=False)
    # String(100) → emails up to 100 characters
    # unique=True → one account per email address

    password = Column(String(255), nullable=False)
    # String(255) → long enough for hashed passwords
    # nullable=False → required, can't create user without password

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
        # default → value used automatically when row is created
        # lambda: → small function called FRESH each time
        # datetime.now(timezone.utc) → current UTC timestamp
        # Without lambda, it would use the time the FILE loaded
        # With lambda, it uses the time the ROW is created ✓
    )

    # ---- RELATIONSHIP ----

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    # "Task"              → connects to the Task model below
    # back_populates="owner" → Task model has a field called 'owner'
    #                          that points back to this User
    # cascade="all, delete-orphan" → if user is deleted,
    #                                delete all their tasks too
    # Usage: user.tasks → returns list of all Task objects for this user

    # ---- __repr__ ----

    def __repr__(self):
        # Called when you do print(user) or repr(user)
        # Shows id, username, email — NO password (security!)
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# ============================================================
# MODEL 2: Task
# ============================================================

class Task(Base):
    __tablename__ = "tasks"

    # ---- COLUMNS ----

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(200), nullable=False)
    # String(200) → task titles up to 200 characters
    # nullable=False → every task must have a title

    description = Column(Text, nullable=True)
    # Text → unlimited length text (for long descriptions)
    # nullable=True → description is optional

    status = Column(String(50), default="pending", nullable=False)
    # default="pending" → new tasks start as pending automatically
    # You don't need to pass status when creating a task

    priority = Column(String(20), default="medium", nullable=False)
    # default="medium" → new tasks default to medium priority

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Integer         → stores the user's id number
    # ForeignKey("users.id") → MUST match a real id in users table
    #                          database rejects invalid values
    # nullable=True   → task can exist without an owner (unassigned)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        # default → set when task is first created

        onupdate=lambda: datetime.now(timezone.utc)
        # onupdate → automatically updates to current time
        # every time this row is modified
        # Like a "last edited" stamp — SQLAlchemy handles it for you
    )

    # ---- RELATIONSHIP ----

    owner = relationship("User", back_populates="tasks")
    # "User"              → connects back to User model
    # back_populates="tasks" → User model has a field called 'tasks'
    # Usage: task.owner → returns the User object who owns this task

    # ---- __repr__ ----

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"


if __name__ == "__main__":
    user = User(username="alice", email="alice@mail.com", password="secure123")
    task = Task(title="Write report", status="pending", priority="high")
    print(repr(user))
    print(repr(task))




















# models.py
# ============================================================
# Q5 — SQLAlchemy Models: User and Task
# ============================================================

# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from datetime import datetime, timezone
# from Q4.database import Base

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     created_at = Column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc)
#     )

#     tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

#     def __repr__(self):

#         return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#     status = Column(String(50), default="pending", nullable=False)

#     priority = Column(String(20), default="medium", nullable=False)

#     owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
#     created_at = Column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc)
#     )

#     updated_at = Column(
#         DateTime(timezone=True),
#         default=lambda: datetime.now(timezone.utc),
#         onupdate=lambda: datetime.now(timezone.utc)
#     )

#     owner = relationship("User", back_populates="tasks")
    
#     def __repr__(self):
#         return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"

# if __name__ == "__main__":
#     user = User(username="alice", email="alice@mail.com", password="secure123")
#     task = Task(title="Write report", status="pending", priority="high")
#     print(repr(user))
#     print(repr(task))