from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# IMPORT YOUR MODELS AND SETTINGS
from database import Base
from models.db_models import User, Loan
from config import settings

# This is the Alembic Config object
config = context.config

# FIX: Escape the '%' in the password for Alembic's config parser
# This prevents the 'invalid interpolation syntax' error
db_url = settings.DATABASE_URL.replace("%", "%%")
config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def include_object(object, name, type_, reflected, compare_to):
    """Only include tables that belong to the LoanHub schema."""
    if type_ == "table" and object.schema != "LoanHub":
        return False
    return True

def run_migrations_online() -> None:
    # Use the correct attribute: config_ini_section
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            include_schemas=True,
            include_object=include_object,
            version_table_schema='LoanHub'
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    pass
else:
    run_migrations_online()