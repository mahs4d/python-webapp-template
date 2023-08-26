from abc import ABC, abstractmethod

from packaging.version import Version

from python_webapp_template.apps.warehouse_layout.api.router import (
    router as warehouse_layout_router,
)
from python_webapp_template.apps.warehouse_layout.repositories import (
    WarehouseLayoutRepository,
    Neo4JWarehouseLayoutRepository,
)
from python_webapp_template.apps.warehouse_layout.services import WarehouseLayoutServices
from python_webapp_template.config import Config
from python_webapp_template.core.di import Container, singleton
from python_webapp_template.managers.fastapi_manager import FastAPIManager
from python_webapp_template.managers.neo4j_manager import Neo4JManager
from python_webapp_template.runner import Runner


class RootContainer(Container, ABC):
    @abstractmethod
    def config(self) -> Config:
        pass

    @abstractmethod
    def fastapi_manager(self) -> FastAPIManager:
        pass

    @abstractmethod
    def neo4j_manager(self) -> Neo4JManager:
        pass

    @abstractmethod
    def warehouse_layout_services(self) -> WarehouseLayoutServices:
        pass

    @abstractmethod
    def warehouse_layout_repository(self) -> WarehouseLayoutRepository:
        pass


class AppRootContainer(RootContainer):
    @singleton
    def config(self) -> Config:
        return Config()

    @singleton
    def runner(self) -> Runner:
        return Runner(
            managers=[
                self.fastapi_manager(),
                self.neo4j_manager(),
            ],
        )

    @singleton
    def fastapi_manager(self) -> FastAPIManager:
        config = self.config()
        return FastAPIManager(
            root_container=self,
            debug=config.debug,
            host=config.api_host,
            port=config.api_port,
            title=config.api_title,
            summary=config.api_summary,
            description=config.api_description,
            version=Version(config.api_version),
            routers=[
                warehouse_layout_router,
            ],
        )

    @singleton
    def neo4j_manager(self) -> Neo4JManager:
        config = self.config()
        return Neo4JManager(
            host=config.neo4j_host,
            port=config.neo4j_port,
            username=config.neo4j_username,
            password=config.neo4j_password,
            database=config.neo4j_database,
        )

    @singleton
    def warehouse_layout_services(self) -> WarehouseLayoutServices:
        return WarehouseLayoutServices(
            warehouse_layout_repository=self.warehouse_layout_repository(),
        )

    @singleton
    def warehouse_layout_repository(self) -> WarehouseLayoutRepository:
        return Neo4JWarehouseLayoutRepository(
            neo4j_manager=self.neo4j_manager(),
        )
