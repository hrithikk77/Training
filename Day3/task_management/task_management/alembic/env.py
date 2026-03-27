import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

from database import Base
import models.db_models

config = context.config
raw_url = os.getenv("DATABASE_URL")
# The password % fix is ONLY for the config option below
config.set_main_option("sqlalchemy.url", raw_url.replace("%", "%%"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        version_table_schema="Task",
        include_schemas=True
    )
    with context.begin_transaction():
        context.run_migrations()
async def run_async_migrations():
    url = os.getenv("DATABASE_URL")
    
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
        connect_args={
            "server_settings": {"search_path": "Task"}
        }
    )

    async with connectable.connect() as connection:
         
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

run_migrations_online()