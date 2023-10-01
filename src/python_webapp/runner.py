import asyncio
import logging

from python_webapp.core.manager import Manager

logger = logging.getLogger(__name__)


class Runner:
    """Runner class is responsible for starting and ending the application."""

    def __init__(
        self,
        managers: list[Manager],
    ) -> None:
        self.managers = managers

    def run(self) -> None:
        """Run the whole application.

        This is the main entrypoint of the application.
        """
        logger.info("Starting the application")
        loop = asyncio.new_event_loop()

        try:
            logger.debug("- Running `setup` on all managers")
            loop.run_until_complete(self._setup())

            logger.debug("- Running `run` on all managers (in parallel)")
            loop.run_until_complete(self._run())
        finally:
            logger.debug("- Running `teardown` on all managers")
            loop.run_until_complete(self._teardown())

        loop.close()

    async def _setup(self) -> None:
        for manager in self.managers:
            await manager.setup()

    async def _run(self) -> None:
        async with asyncio.TaskGroup() as tg:
            for manager in self.managers:
                tg.create_task(manager.run())

    async def _teardown(self) -> None:
        for manager in self.managers:
            await manager.teardown()
