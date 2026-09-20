import click

from .image_cli import image
from .folder_cli import folder


@click.group()
@click.version_option()
def cli() -> None:
    """Generate and apply geometric watermarks."""


cli.add_command(image)
cli.add_command(folder)