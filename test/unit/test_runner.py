from unittest.mock import AsyncMock

import pytest

from python_webapp.core.manager import Manager
from python_webapp.runner import Runner


def test_run() -> None:
    manager1 = AsyncMock(Manager)
    manager2 = AsyncMock(Manager)

    runner = Runner(
        managers=[
            manager1,
            manager2,
        ],
    )

    runner.run()

    manager1.setup.assert_called()
    manager2.setup.assert_called()
    manager1.run.assert_called()
    manager2.run.assert_called()
    manager1.teardown.assert_called()
    manager2.teardown.assert_called()


def test_run_with_error() -> None:
    manager1 = AsyncMock(Manager)
    manager2 = AsyncMock(Manager)
    manager2.run = AsyncMock(side_effect=ValueError("error"))

    runner = Runner(
        managers=[
            manager1,
            manager2,
        ],
    )

    with pytest.raises(ExceptionGroup):
        runner.run()

    manager1.setup.assert_called()
    manager2.setup.assert_called()
    manager1.run.assert_called()
    manager2.run.assert_called()
    manager1.teardown.assert_called()
    manager2.teardown.assert_called()
