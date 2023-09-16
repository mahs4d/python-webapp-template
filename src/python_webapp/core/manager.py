from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    async def setup(self) -> None:
        pass

    @abstractmethod
    async def run(self) -> None:
        pass

    @abstractmethod
    async def teardown(self) -> None:
        pass
