import asyncio

from python_webapp_template.container import AppRootContainer


def main():
    container = AppRootContainer()
    runner = container.runner()

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(runner.setup())
        loop.run_until_complete(runner.run())
    except KeyboardInterrupt:
        loop.run_until_complete(runner.teardown())
    finally:
        loop.close()


if __name__ == "__main__":
    main()
