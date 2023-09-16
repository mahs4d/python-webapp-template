from typing import Type

from alembic import context
from sqlalchemy import pool, engine_from_config

from python_webapp.core.db import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config


def get_all_db_models() -> list[Type[Base]]:
    """This function should return all db orm classes."""
    from python_webapp.apps.user_management.repositories.db_models import UserDBModel

    return [UserDBModel]


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    get_all_db_models()
    target_metadata = Base.metadata
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    get_all_db_models()
    target_metadata = Base.metadata
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
