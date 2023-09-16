import random

from python_webapp.core.di import Container, singleton


def test_singleton() -> None:
    class TestContainer(Container):
        @singleton
        def random(self) -> float:
            return random.random()

    container = TestContainer()

    r1 = container.random()
    r2 = container.random()

    assert r1 == r2
