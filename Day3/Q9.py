import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- IMPORTANT: FOR SYNCHRONOUS SCRIPTS, USE postgresql:// (NOT +asyncpg) ---
# We replace +asyncpg with nothing to use the standard psycopg2 driver
DATABASE_URL = os.getenv("DATABASE_URL").replace("+asyncpg", "")


engine = create_engine(
    DATABASE_URL,
    # 1. pool_size: The number of connections to keep open in the "pool".
    #    Matters: Saves time by not having to re-connect to Supabase every request.
    pool_size=5,
    # 2. max_overflow: Extra connections allowed beyond pool_size during high traffic.
    #    Matters: Allows the app to handle temporary "spikes" without crashing.
    max_overflow=10,
    
    # 3. pool_timeout: Max seconds to wait for a connection before throwing an error.
    #    Matters: Prevents the app from "hanging" forever if the DB is busy.
    pool_timeout=30,
    
    # 4. pool_recycle: Closes and re-opens connections older than 1800s (30 mins).
    #    Matters: Prevents "Stale" connections that the DB might have closed.
    pool_recycle=1800,
    
    # 5. pool_pre_ping: Checks if the connection is alive before using it.
    #    Matters: CRITICAL for Supabase/Cloud DBs because they often drop idle 
    #    connections. This transparently reconnects if the link is broken.
    pool_pre_ping=True
)

# Create Session factory
Session = sessionmaker(bind=engine)

def run_pool_test():
    # List to store our active sessions
    sessions = []
    
    print("--- Starting Pool Monitoring ---")
    
    # Open 3 sessions and check pool status
    for i in range(3):
        s = Session()
        
        # IMPORTANT: A connection is not "checked out" from the pool until 
        # we actually execute a query.
        s.execute(text("SELECT 1")) 
        
        sessions.append(s)
        
        # Print status after each open
        # format: Pool size, Connections in pool, Current Overflow, Current Checked out
        print(f"After opening session {i+1}: {engine.pool.status()}")

    # Close all sessions to return connections to the pool
    for s in sessions:
        s.close()

    print(f"\nAfter closing all: {engine.pool.status()}")

if __name__ == "__main__":
    try:
        run_pool_test()
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")