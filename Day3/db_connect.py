# db_connect.py
# ============================================================
# SMART CONNECTION HELPER
# Tries multiple ports automatically
# Works on both office WiFi and mobile hotspot
# ============================================================

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# We store connection configs as a LIST of options
# Python will try them ONE BY ONE until one works
# Like trying different keys on a lock!
# ============================================================

BASE_HOST = "db.fhttovtmmddkqrlnemzi.supabase.co"
# Your Supabase host — same for all attempts
# We separate the host so we can easily swap ports below

BASE_USER = "postgres"
BASE_PASSWORD = "hrithik@K77"
# Note: in code we use the REAL password (with @)
# The %40 encoding is only needed inside URL strings
# psycopg2 handles special characters fine when passed separately

BASE_DB = "postgres"

CONNECTION_OPTIONS = [
    {
        "name": "Port 5432 (standard PostgreSQL)",
        "host": BASE_HOST,
        "port": 5432,
        # Standard PostgreSQL port
        # Works on: home WiFi, mobile hotspot
        # Blocked by: most office networks
    },
    {
        "name": "Port 6543 (Supabase pooler)",
        "host": BASE_HOST,
        "port": 6543,
        # Supabase's connection pooler port
        # Sometimes works when 5432 is blocked
        # Still blocked by strict office networks
    },
    {
        "name": "Port 443 (HTTPS port - most open)",
        "host": "aws-0-ap-south-1.pooler.supabase.com",
        "port": 5432,
        # Different host — Supabase's pooler server
        # Uses AWS infrastructure
        # More likely to work on office networks
        # because it routes differently
    },
]
# We try each option in order
# First one that connects successfully — we use that!
# If ALL fail → office network is too strict → use hotspot


def get_connection():
    """
    Tries multiple connection options automatically.
    Returns a working connection or raises an error.

    Usage in other files:
        from db_connect import get_connection
        conn = get_connection()
    """

    errors = []
    # We collect all error messages
    # So if everything fails, we show ALL errors (helpful for debugging)

    for option in CONNECTION_OPTIONS:
        # Loop through each connection option one by one
        # option is a dictionary like:
        # {"name": "Port 5432", "host": "...", "port": 5432}

        try:
            print(f"🔄 Trying: {option['name']}...")
            # Tell the user which option we're currently trying
            # option['name'] accesses the "name" key from the dict

            conn = psycopg2.connect(
                host=option["host"],
                port=option["port"],
                database=BASE_DB,
                user=BASE_USER,
                password=BASE_PASSWORD,
                connect_timeout=5,
                # connect_timeout=5 means:
                # "If no response in 5 seconds, give up and try next"
                # Without this, Python waits ~30 seconds per attempt!
                # With this, total wait time = 5s × 3 options = 15s max
            )
            # psycopg2.connect() with SEPARATE parameters instead of URL
            # This is an ALTERNATIVE to passing the full URL string
            # Both ways work — separate params are cleaner and safer
            # because you don't need to worry about special char encoding

            print(f" Connected via: {option['name']}\n")
            # Tell user which option worked

            return conn
            # Return the working connection immediately
            # This exits the function — no more options tried

        except psycopg2.OperationalError as e:
            error_msg = f" {option['name']} failed: {str(e)[:80]}"
            # str(e)[:80] → convert error to string, take first 80 chars
            # Full error messages are very long — we trim them for readability

            errors.append(error_msg)
            # Add this error to our collection
            print(error_msg)
            # Show it immediately so user knows what's happening
            continue
            # continue → skip to next iteration of the for loop
            # i.e., try the next connection option

    # ============================================================
    # If we reach here, ALL options failed
    # ============================================================

    print("\n" + "=" * 50)
    print("💡 ALL CONNECTION OPTIONS FAILED")
    print("=" * 50)
    print("Most likely cause: Office/corporate network")
    print("blocking all database ports.")
    print("\nSOLUTION: Switch to mobile hotspot and try again.")
    print("=" * 50)

    raise Exception("Could not connect to database with any option.")
    # raise = create and throw an error
    # This stops execution and lets the caller handle it
    # Better than returning None (which could cause confusing errors later)


# ============================================================
# TEST — run this file directly to test connection
# python db_connect.py
# ============================================================

if __name__ == "__main__":
    # __name__ == "__main__" means:
    # "only run this block if THIS file is run directly"
    # If another file does `from db_connect import get_connection`,
    # this block is SKIPPED — only the function is imported
    # This is a very common Python pattern!

    print("🧪 Testing database connection...\n")
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT version();")
        # version() is a built-in PostgreSQL function
        # Returns the PostgreSQL version string
        # Great for testing — always works if connected

        version = cursor.fetchone()[0]
        print(f"PostgreSQL version: {version[:50]}")
        # [:50] → first 50 characters (version string is very long)

        cursor.close()
        conn.close()
        print(" Connection closed. Everything working perfectly!")

    except Exception as e:
        print(f"Error: {e}")