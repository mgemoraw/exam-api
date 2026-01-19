# alembic/env.py
import os
import sys 
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


import logging
import os
import sys 


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

    
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


try:
    fileConfig(config.config_file_name)
except Exception:
    logging.basicConfig(level=logging.WARNING)


# Add your project to the python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# ============ CRITICAL CHANGE 1: Import settings FIRST ============
from app.core.config import settings  # Your config file

# ============ CRITICAL CHANGE 2: Override alembic.ini URL ============
# Use your actual database URL from settings, not the hardcoded one
# Remove or comment out any hardcoded DB_URL lines
# DB_URL = os.getenv('SQLITE_DB_URL', 'sqlite:///./test.db')
config.set_main_option('sqlalchemy.url', settings.SQLITE_DATABASE_URL)

# Import your Base and models
from app.models import Base 

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url") or settings.database.SYNC_DATABASE_URL

    # ============ CRITICAL CHANGE 4: SQLite batch mode ============
    render_as_batch = 'sqlite' in url.lower() if url else False

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=render_as_batch,  # ✅ Enables batch mode for SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # ============ CRITICAL CHANGE 5: Handle SQLite batch mode ============
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Check if using SQLite
        is_sqlite = connection.engine.dialect.name == 'sqlite'
        
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            render_as_batch=is_sqlite,  # ✅ Enables batch mode for SQLite
            compare_type=True,           # ✅ Better type comparison
            compare_server_default=True  # ✅ Compare default values
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()


