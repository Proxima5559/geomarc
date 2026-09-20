from pathlib import Path
import click
from rich.console import Console

from geomarc.image.folder import process_folder
from geomarc.cli.common import common_watermark_options

console = Console()

@click.command()
@click.argument(
    "input_dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        path_type=Path,
    ),
)
@click.argument(
    "output_dir",
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        path_type=Path,
    ),
)
@common_watermark_options
@click.option(
    "--on-unsupported",
    "-u",
    type=click.Choice(
        ["skip", "fail"],
        case_sensitive=False,
    ),
    default="skip",
    show_default=True,
    help="Action to take when an unsupported file format is encountered.",
)
def folder(
    input_dir: Path,
    output_dir: Path,
    complexity: str,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    on_unsupported: str,
) -> None:
    """Apply a geometric watermark to all images in a folder."""

    if output_dir.resolve() == input_dir.resolve():
        raise click.UsageError(
            "Input and output directories must be different."
        )

    try:
        with console.status("[bold]Processing folder..."):
            processed, skipped = process_folder(
                input_dir=input_dir,
                output_dir=output_dir,
                complexity=complexity.lower(),
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                on_unsupported=on_unsupported.lower(),
            )

    except (ValueError, NotADirectoryError, FileNotFoundError) as error:
        raise click.ClickException(str(error)) from error

    console.print(
        f"[green]✓[/green] Folder processed: "
        f"processed [bold]{processed}[/bold], "
        f"skipped [bold]{skipped}[/bold] -> "
        f"[bold]{output_dir}[/bold]"
    )