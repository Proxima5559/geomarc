from importlib.metadata.diagnose import inspect
from pathlib import Path
from PIL import Image
import click
from rich.console import Console

from geomarc.cli.errors import handle_cli_errors
from geomarc.cli.inspect import show_inspection
from geomarc.generator.placement import generate_placements
from geomarc.image.watermark import apply_watermark
from geomarc.cli.common import (
    common_watermark_options,
    parse_protected_regions,
)

console = Console()


@click.group()
@click.version_option()
def cli() -> None:
    """Generate and apply geometric watermarks."""


@cli.command()
@click.argument(
    "input_path",
    type=click.Path(
        exists=True,
        dir_okay=False,
        path_type=Path,
    ),
)
@click.argument(
    "output_path",
    type=click.Path(
        dir_okay=False,
        path_type=Path,
    ),
)
@common_watermark_options
def image(
    input_path: Path,
    output_path: Path,
    complexity: str,
    style: str | None, 
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protect: tuple[str, ...],
    inspect: bool,
) -> None:
    """Apply a geometric watermark to a single image."""

    if not inspect and output_path.resolve() == input_path.resolve():
        raise click.UsageError(
            "Input and output files must be different."
        )
   
    protected_regions = parse_protected_regions(protect)

    with handle_cli_errors():
        if inspect:
            with Image.open(input_path) as image_file:
                image_width, image_height = image_file.size
                image_format = image_file.format

            placements = generate_placements(
                image_width=image_width,
                image_height=image_height,
                count=count,
                seed=seed,
                protected_regions=protected_regions,
            )

            show_inspection(
                console,
                image_width=image_width,
                image_height=image_height,
                image_format=image_format,
                complexity=complexity.lower(),
                style=style.lower() if style else None,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                placements=placements,
            )

            return

        with console.status("[bold]Generating watermark..."):
            apply_watermark(
                input_path=input_path,
                output_path=output_path,
                complexity=complexity.lower(),
                style=style,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                protected_regions=protected_regions,
            )


    console.print(
        f"[green]✓[/green] Watermark applied: "
        f"[bold]{output_path}[/bold]"
    )