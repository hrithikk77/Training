from dotenv import load_dotenv
from pathlib import Path
import psycopg2
import psycopg2.errors
import os


dotenv_path = Path(__file__).parent / ".env"


load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def run_raw_query():
    conn = None
    cursor = None

    try:
        # STEP 1: Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        print("Connected to Supabase successfully!")

        # STEP 2: Create cursor
        cursor = conn.cursor()
   
        query = "SELECT * FROM users LIMIT 5;"
   
        cursor.execute(query)

        # STEP 4: Fetch results
        rows = cursor.fetchall()

        # STEP 5: Print results
        print("\nCustomers (raw SQL):")
        for row in rows:
            print(row)

        print(f"\nRows fetched: {len(rows)}")

    except psycopg2.errors.UndefinedTable:
        print("Error: The 'customer' table does not exist.")
        print("Please check your database setup.")

    except psycopg2.OperationalError as e:
        print(f"Connection error: {e}")
        print("Check your DATABASE_URL in the .env file.")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Connection closed.")

run_raw_query()