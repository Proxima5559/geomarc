import click

from .image_cli import image
from .folder_cli import folder
from .pdf_cli import pdf

@click.group()
@click.version_option(version="0.1.1")
def cli() -> None:
    """Generate and apply geometric watermarks."""


cli.add_command(image)
cli.add_command(folder)
cli.add_command(pdf)