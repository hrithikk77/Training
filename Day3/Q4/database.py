# ============================================================
# database.py
# SQLAlchemy Setup — Engine, Session & Base
# ============================================================

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, text
# create_engine → creates the engine (connection factory)
# text()        → wraps raw SQL strings so SQLAlchemy can use them safely
# Without text(), SQLAlchemy will raise an error if you pass a plain string

from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker     → creates a Session CLASS (a factory for sessions)
# declarative_base → creates the Base class all your models will inherit from

import os

# ============================================================
# STEP 1: Load .env file
# ============================================================

dotenv_path = Path(__file__).parent / ".env"
# __file__ = this file (database.py)
# .parent  = the folder containing database.py
# / ".env" = .env file in the same folder

load_dotenv(dotenv_path=dotenv_path)
# Loads DATABASE_URL into environment

DATABASE_URL = os.getenv("DATABASE_URL")
# Reads the URL from environment
# e.g. "postgresql://postgres.xxx:pass@host:6543/postgres"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file!")
# If DATABASE_URL is None or empty string, stop immediately
# Better to crash here with a clear message than get a
# confusing error later deep inside SQLAlchemy

# ============================================================
# STEP 2: Create the Engine
# ============================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    # echo=False → don't print every SQL statement to console
    # echo=True  → prints all SQL (useful for debugging)
    # Like a car with the hood open vs closed
    # For learning you can set echo=True to see what's happening!

    pool_pre_ping=True,
    # pool_pre_ping=True → before using a connection from the pool,
    # send a quick "ping" (SELECT 1) to check it's still alive
    # Prevents "connection dropped" errors after idle time
    # Like checking if the phone line is active before speaking

    pool_size=5,
    # pool_size=5 → keep 5 connections open and ready in the pool
    # A "pool" is a set of pre-made connections ready to use
    # Like having 5 taxis waiting outside instead of calling one each time
    # Reusing connections is MUCH faster than creating new ones each query

    max_overflow=10,
    # max_overflow=10 → if all 5 pool connections are busy,
    # allow up to 10 MORE temporary connections
    # So max total = pool_size(5) + max_overflow(10) = 15 connections
    # These extra connections are closed after use (not kept in pool)
)

# ============================================================
# STEP 3: Create Session Factory
# ============================================================

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
# SessionLocal is now a CLASS (a factory)
# You create actual session OBJECTS from it like:
# db = SessionLocal()   ← creates one session
# db.close()            ← closes it when done

print("Session factory ready.")

# ============================================================
# STEP 4: Create Base class
# ============================================================

Base = declarative_base()
# Base is the parent class for ALL your database models
# Later when you create tables as Python classes, they'll look like:
#
# class User(Base):          ← inherits from Base
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
# SQLAlchemy uses Base to track all your models and
# knows how to create/query those tables

# ============================================================
# STEP 5: verify_connection() function
# ============================================================

def verify_connection():
    """
    Tests the database connection by running SELECT 1.
    SELECT 1 is the simplest possible SQL query —
    it doesn't touch any table, just returns the number 1.
    If this works, the database is reachable and credentials are correct.
    It's like knocking on a door to check if anyone's home.
    """

    # First, print the engine URL with password masked
    url_str = str(engine.url)
    # engine.url gives us the connection URL as an object
    # str() converts it to a string like:
    # "postgresql://postgres.xxx:mypassword@host:6543/postgres"

    # Mask the password for security
    # We never want to print real passwords to console/logs!
    masked_url = str(engine.url).replace(
        str(engine.url.password),
        "***"
    ) if engine.url.password else url_str
    # engine.url.password → extracts just the password part
    # .replace(actual_password, "***") → hides it
    # Result: "postgresql://postgres.xxx:***@host:6543/postgres"

    print(f"Engine created: {masked_url}")

    try:
        with engine.connect() as connection:
            # engine.connect() opens ONE real connection from the pool
            # 'with' = context manager → automatically closes connection
            # when the block ends (even if an error occurs!)
            # Like borrowing a book — it goes back to library automatically

            result = connection.execute(text("SELECT 1"))
            # text("SELECT 1") → wraps the SQL string safely
            # .execute() → runs the query
            # Returns a "Result" object (not the value directly)

            value = result.scalar()
            # .scalar() → gets the single value from the result
            # SELECT 1 returns one row with one column = 1
            # .scalar() extracts just that number: 1
            # If you used .fetchone() you'd get (1,) — a tuple
            # .scalar() gives you just 1 — cleaner!

            print(f"Connection verified: SELECT 1 returned {value}")
            print("Database connection successful!")

    except Exception as e:
        # If anything goes wrong during connection or query
        print(f"Connection failed: {e}")
        print("Check your DATABASE_URL and network connection.")
        raise
        # raise → re-raises the same error after printing
        # So the calling code also knows something went wrong
        # Like showing someone the error message AND passing it along


# ============================================================
# This block only runs when you run database.py directly
# It does NOT run when another file imports from database.py
# ============================================================

if __name__ == "__main__":
    verify_connection()
























# from dotenv import load_dotenv
# from pathlib import Path
# from sqlalchemy import create_engine, text

# from sqlalchemy.orm import sessionmaker, declarative_base

# import os

# dotenv_path = Path(__file__).parent / ".env"

# load_dotenv(dotenv_path=dotenv_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL not found in .env file!")

# engine = create_engine(
#     DATABASE_URL,
#     echo=False,

#     pool_pre_ping=True,

#     pool_size=5,

#     max_overflow=10,

# )


# SessionLocal = sessionmaker(
#     autocommit=False,

#     autoflush=False,

#     bind=engine,

# )

# print("Session factory ready.")

# Base = declarative_base()

# def verify_connection():
#     """
#     Tests the database connection by running SELECT 1.
#     SELECT 1 is the simplest possible SQL query —
#     it doesn't touch any table, just returns the number 1.
#     If this works, the database is reachable and credentials are correct.
#     It's like knocking on a door to check if anyone's home.
#     """

#     url_str = str(engine.url)

#     masked_url = str(engine.url).replace(
#         str(engine.url.password),
#         "***"
#     ) if engine.url.password else url_str
   
#     print(f"Engine created: {masked_url}")

#     try:
#         with engine.connect() as connection:
          

#             result = connection.execute(text("SELECT 1"))
            
#             value = result.scalar()
           
#             print(f"Connection verified: SELECT 1 returned {value}")
#             print("Database connection successful!")

#     except Exception as e:
#         # If anything goes wrong during connection or query
#         print(f"Connection failed: {e}")
#         print("Check your DATABASE_URL and network connection.")
#         raise
        
# if __name__ == "__main__":
#     verify_connection()