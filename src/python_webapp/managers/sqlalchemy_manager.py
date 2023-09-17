import logging
from pathlib import Path

from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import Connection, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from python_webapp.core.health import HealthReport, HealthReportable
from python_webapp.core.manager import Manager

logger = logging.getLogger(__name__)


class SQLAlchemyManager(HealthReportable, Manager):
    """Manager for accessing database using `SQLAlchemy` library."""

    def __init__(
        self,
        sqlalchemy_url: str,
        declarative_base_classes: list[type[DeclarativeBase]],
    ) -> None:
        self.sqlalchemy_url = sqlalchemy_url
        self.declarative_base_classes = declarative_base_classes

        self._is_setup = False
        self._engine: AsyncEngine = None  # type: ignore
        self._async_sessionmaker: async_sessionmaker = None  # type: ignore

    async def setup(self) -> None:
        """Setup database manager."""
        logger.info("Setting up `SQLAlchemyManager`")
        if self._is_setup:
            logger.warning("Setup is called multiple times!")
            return

        logger.debug("- Creating SQLAlchemy engine and session maker")
        self._engine = create_async_engine(url=self.sqlalchemy_url)
        self._async_sessionmaker = async_sessionmaker(bind=self._engine)

        logger.debug("- Running migrations")
        await self._run_migrations()

        self._is_setup = True

    async def run(self) -> None:
        """Run doesn't do anything here."""

    async def teardown(self) -> None:
        """Teardown database manager."""
        logger.info("Tearing down `SQLAlchemyManager`")
        if not self._is_setup:
            logger.warning("Teardown is called before setup!")
            return

        self._engine = None  # type: ignore
        self._async_sessionmaker = None  # type: ignore

        self._is_setup = False

    async def get_health_report(self) -> HealthReport:
        """Get database health report."""
        is_healthy = True

        if not self._is_setup:
            is_healthy = False

        try:
            async with self._engine.connect() as connection:
                await connection.execute(text("SELECT 1;"))
        except OperationalError:
            is_healthy = False

        return HealthReport(
            component="db",
            is_healthy=is_healthy,
        )

    def get_async_session(self) -> AsyncSession:
        if not self._is_setup:
            raise Exception("Setup is not called!")

        return self._async_sessionmaker()

    async def _run_migrations(self) -> None:
        def run_alembic_upgrade(connection: Connection) -> None:
            alembic_config = AlembicConfig(
                file_=Path(__file__).parent.parent.parent.parent / "alembic.ini",
            )
            alembic_config.set_main_option(
                name="script_location",
                value=str(Path(__file__).parent.parent / "migrations"),
            )
            alembic_config.set_main_option(
                name="sqlalchemy.url",
                value=self.sqlalchemy_url,
            )
            alembic_config.attributes["connection"] = connection

            upgrade(
                config=alembic_config,
                revision="head",
            )

        async with self._engine.connect() as conn:
            await conn.run_sync(run_alembic_upgrade)


class PostgresManager(SQLAlchemyManager):
    def __init__(
        self,
        host: str,
        port: int,
        db_name: str,
        user: str,
        password: str,
        declarative_base_classes: list[type[DeclarativeBase]],
    ) -> None:
        super().__init__(
            sqlalchemy_url=f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}",
            declarative_base_classes=declarative_base_classes,
        )
