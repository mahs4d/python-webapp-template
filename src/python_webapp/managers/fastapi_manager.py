import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from packaging.version import Version

from python_webapp.core.api.api_models import ErrorResponse
from python_webapp.core.di import Container
from python_webapp.core.errors import AppError
from python_webapp.core.health import HealthReportable, HealthReport
from python_webapp.core.manager import Manager

logger = logging.getLogger(__name__)


class FastAPIManager(HealthReportable, Manager):
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
        self._app: FastAPI = None
        self._uvicorn_server: uvicorn.Server = None

    async def setup(self):
        logger.info("Setting up `FastAPIManager`")
        if self._is_setup:
            raise Exception("Setup is called multiple times!")

        # Setup fastapi app.
        logger.debug("- Setting up fastapi app")
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

        self._app.add_exception_handler(AppError, self._app_error_handler)

        # Setup uvicorn server.
        logger.debug("- Setting up uvicorn")
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
        logger.info("Tearing down `FastAPIManager`")
        if not self._is_setup:
            raise Exception("Teardown is called before setup!")

        self._app = None
        self._uvicorn_server = None

        self._is_setup = False

    async def get_health_report(self) -> HealthReport:
        is_healthy = True

        if not self._is_setup:
            is_healthy = False

        if not self._uvicorn_server.started:
            is_healthy = False

        return HealthReport(
            component="api",
            is_healthy=is_healthy,
        )

    @staticmethod
    async def _app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            content={
                "error": ErrorResponse(
                    code=exc.code,
                    message=exc.message,
                ).model_dump(),
            },
            status_code=exc.status,
        )
