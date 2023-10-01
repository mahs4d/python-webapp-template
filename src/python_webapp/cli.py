from typer import Context, Typer

cli = Typer()


@cli.command()
def run(ctx: Context) -> None:
    container = ctx.obj["container"]
    runner = container.runner()
    runner.run()
