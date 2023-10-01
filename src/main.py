from typer import Typer

from python_webapp.cli import cli as app_cli
from python_webapp.container import AppRootContainer


def main() -> None:
    context_settings = {
        "obj": {
            "container": AppRootContainer(),
        },
    }
    typer_app = Typer(context_settings=context_settings)
    typer_app.add_typer(app_cli, name="app")
    typer_app()


if __name__ == "__main__":
    main()
