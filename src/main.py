from python_webapp.container import AppRootContainer


def main():
    container = AppRootContainer()
    runner = container.runner()
    runner.main()


if __name__ == "__main__":
    main()
