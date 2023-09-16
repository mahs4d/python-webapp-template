from abc import ABC, abstractmethod

from python_webapp.apps.system.api.router import (
    router as system_router,
)
from python_webapp.apps.system.services import SystemServices
from python_webapp.apps.user_management.api.router import router as user_management_router
from python_webapp.apps.user_management.repositories.db_models import (
    Base as UserManagementDeclarativeBase,
)
from python_webapp.apps.user_management.repositories.user_repository import (
    SQLAlchemyUserRepository,
    UserRepository,
)
from python_webapp.apps.user_management.services import UserManagementServices
from python_webapp.config import Config
from python_webapp.core.di import Container, singleton
from python_webapp.managers.fastapi_manager import FastAPIManager
from python_webapp.managers.sqlalchemy_manager import PostgresManager, SQLAlchemyManager
from python_webapp.runner import Runner


class RootContainer(Container, ABC):
    @abstractmethod
    def config(self) -> Config:
        pass

    @abstractmethod
    def runner(self) -> Runner:
        pass

    @abstractmethod
    def fastapi_manager(self) -> FastAPIManager:
        pass

    @abstractmethod
    def sqlalchemy_manager(self) -> SQLAlchemyManager:
        pass

    @abstractmethod
    def system_services(self) -> SystemServices:
        pass

    @abstractmethod
    def user_repository(self) -> UserRepository:
        pass

    @abstractmethod
    def user_management_services(self) -> UserManagementServices:
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
                self.sqlalchemy_manager(),
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
            version=config.api_version,
            routers=[
                system_router,
                user_management_router,
            ],
        )

    @singleton
    def sqlalchemy_manager(self) -> SQLAlchemyManager:
        config = self.config()
        return PostgresManager(
            host=config.postgres_host,
            port=config.postgres_port,
            db_name=config.postgres_db_name,
            user=config.postgres_user,
            password=config.postgres_password,
            declarative_base_classes=[
                UserManagementDeclarativeBase,
            ],
        )

    @singleton
    def system_services(self) -> SystemServices:
        return SystemServices(
            config=self.config(),
            health_reportables=[
                self.fastapi_manager(),
                self.sqlalchemy_manager(),
            ],
        )

    @singleton
    def user_repository(self) -> UserRepository:
        return SQLAlchemyUserRepository(
            sqlalchemy_manager=self.sqlalchemy_manager(),
        )

    @singleton
    def user_management_services(self) -> UserManagementServices:
        return UserManagementServices(
            user_repository=self.user_repository(),
        )
