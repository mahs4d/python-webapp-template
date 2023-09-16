from python_webapp.container import AppRootContainer


def main() -> None:
    container = AppRootContainer()
    runner = container.runner()
    runner.main()


if __name__ == "__main__":
    main()
