from pathlib import Path
import click
from rich.console import Console

from geomarc.image.watermark import apply_watermark
from geomarc.cli.common import common_watermark_options

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
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
) -> None:
    """Apply a geometric watermark to a single image."""

    if output_path.resolve() == input_path.resolve():
        raise click.UsageError(
            "Input and output files must be different."
        )

    try:
        with console.status("[bold]Generating watermark..."):
            apply_watermark(
                input_path=input_path,
                output_path=output_path,
                complexity=complexity.lower(),
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
            )

    except (ValueError, FileNotFoundError) as error:
        raise click.ClickException(str(error)) from error

    console.print(
        f"[green]✓[/green] Watermark applied: "
        f"[bold]{output_path}[/bold]"
    )