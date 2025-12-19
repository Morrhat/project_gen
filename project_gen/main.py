import click
from project_gen.utils.download import download, \
    init
from project_gen.utils.generate import generate


#download()


@click.group()
def cli() -> None:
    ...


@cli.command("generate")
def generate_command() -> None:
    generate()


@cli.command("init")
def init_command() -> None:
    init()



cli.add_command(generate_command)
cli.add_command(init_command)

if __name__ == "__main__":
    cli()