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
    """Manager class for API server using `FastAPI` library."""
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
        """Setup API server."""
        logger.info("Setting up `FastAPIManager`")
        if self._is_setup:
            raise Exception("Setup is called multiple times!")

        logger.debug("- Setting up fastapi app")
        self._app = self._create_fastapi_app()

        logger.debug("- Setting up uvicorn")
        self._uvicorn_server = self._create_uvicorn_server()

        self._is_setup = True

    async def run(self):
        """Run API server."""
        if not self._is_setup:
            raise Exception("Run is called before setup!")

        await self._uvicorn_server.serve()

    async def teardown(self):
        """Stop and teardown """
        logger.info("Tearing down `FastAPIManager`")
        if not self._is_setup:
            raise Exception("Teardown is called before setup!")

        self._app = None
        self._uvicorn_server = None

        self._is_setup = False

    async def get_health_report(self) -> HealthReport:
        """Get API health report."""
        is_healthy = True

        if not self._is_setup:
            is_healthy = False
        elif not self._uvicorn_server.started:
            is_healthy = False

        return HealthReport(
            component="api",
            is_healthy=is_healthy,
        )

    def _create_fastapi_app(self) -> FastAPI:
        app = FastAPI(
            debug=self.debug,
            title=self.title,
            summary=self.summary,
            description=self.description,
            version=str(self.version),
        )

        for router in self.routers:
            app.include_router(router=router)

        app.state.root_container = self.root_container

        app.add_exception_handler(AppError, self._app_error_handler)

        return app

    def _create_uvicorn_server(self) -> uvicorn.Server:
        uvicorn_config = uvicorn.Config(
            app=self._app,
            host=self.host,
            port=self.port,
        )
        server = uvicorn.Server(config=uvicorn_config)

        return server

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
