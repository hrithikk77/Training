# main.py
# This matches the exact input from the problem statement:
# from database import engine, SessionLocal, verify_connection

from database import engine, SessionLocal, verify_connection
# Imports three things from database.py:
# engine       → the SQLAlchemy engine object
# SessionLocal → the session factory class
# verify_connection → the function that tests the connection

verify_connection()
# Calls the function — runs SELECT 1 and prints results