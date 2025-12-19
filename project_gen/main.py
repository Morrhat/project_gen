import click
from project_gen.utils.download import download
from project_gen.utils.generate import generate


#download()


@click.group()
def cli() -> None:
    ...


@cli.command("generate")
def generate_command() -> None:
    generate()

cli.add_command(generate_command)

if __name__ == "__main__":
    cli()