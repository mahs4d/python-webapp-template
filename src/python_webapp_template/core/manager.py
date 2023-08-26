from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    @abstractmethod
    async def teardown(self):
        pass
