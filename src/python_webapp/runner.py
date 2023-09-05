import asyncio

from python_webapp.core.manager import Manager


class Runner:
    def __init__(
        self,
        managers: list[Manager],
    ):
        self.managers = managers

    async def setup(self):
        for manager in self.managers:
            await manager.setup()

    async def run(self):
        async with asyncio.TaskGroup() as tg:
            for manager in self.managers:
                tg.create_task(manager.run())

    async def teardown(self):
        for manager in self.managers:
            await manager.teardown()
