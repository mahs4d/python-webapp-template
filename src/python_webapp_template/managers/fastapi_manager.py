import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from packaging.version import Version

from python_webapp_template.core.di import Container
from python_webapp_template.core.manager import Manager

logger = logging.getLogger(__name__)


class FastAPIManager(Manager):
    def __init__(
            self,
            root_container: Container,
            debug: bool,
            title: str,
            summary: str,
            description: str,
            version: Version,
            host: str,
            port: int,
            routers: list[APIRouter],
    ):
        self.root_container = root_container
        self.debug = debug
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.host = host
        self.port = port
        self.routers = routers

        self._is_setup = False
        self._app = None
        self._uvicorn_server = None

    async def setup(self):
        logging.info("Setting up `FastAPIManager`")
        if self._is_setup:
            raise Exception("Setup is called multiple times!")

        # Setup fastapi app.
        logging.debug("- Setting up fastapi app")
        self._app = FastAPI(
            debug=self.debug,
            title=self.title,
            summary=self.summary,
            description=self.description,
            version=str(self.version),
        )

        for router in self.routers:
            self._app.include_router(router=router)

        self._app.state.root_container = self.root_container

        # Setup uvicorn server.
        logging.debug("- Setting up uvicorn")
        uvicorn_config = uvicorn.Config(
            app=self._app,
            host=self.host,
            port=self.port,
        )
        self._uvicorn_server = uvicorn.Server(config=uvicorn_config)

        self._is_setup = True

    async def run(self):
        if not self._is_setup:
            raise Exception("Run is called before setup!")

        await self._uvicorn_server.serve()

    async def teardown(self):
        logging.info("Tearing down `FastAPIManager`")
        if not self._is_setup:
            raise Exception("Teardown is called before setup!")

        self._app = None
        self._uvicorn_server = None

        self._is_setup = False
