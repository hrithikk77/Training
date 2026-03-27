from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from decorators.retry import retry

# 1. Create Engine with Connection Pooling (Requirement 4)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Raw SQL Health Check (Requirement 4)
@retry(max_attempts=3)
def check_db_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Successfully connected to Supabase Database!")

# 3. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()