import logging

from neo4j import AsyncGraphDatabase, AsyncDriver

from python_webapp_template.core.manager import Manager

logger = logging.getLogger(__name__)


class Neo4JManager(Manager):
    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            database: str
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

        self._is_setup = False
        self._driver = None

    async def setup(self):
        logging.info("Setting up `Neo4JManager`")
        if self._is_setup:
            raise Exception("Setup is called multiple times!")

        # Setup driver.
        logging.debug("- Setting up driver")
        self._driver = AsyncGraphDatabase.driver(
            uri=f'neo4j://{self.host}:{self.port}',
            auth=(self.username, self.password),
            database=self.database,
        )
        await self._driver.verify_connectivity()

        self._is_setup = True

    async def run(self):
        if not self._is_setup:
            raise Exception("Run is called before setup!")

    async def teardown(self):
        logging.info("Tearing down `Neo4JManager`")
        if not self._is_setup:
            raise Exception("Teardown is called before setup!")

        await self._driver.close()
        self._driver = None

        self._is_setup = False

    def get_driver(self) -> AsyncDriver:
        if not self._is_setup:
            raise Exception("Setup is not called!")

        return self._driver
