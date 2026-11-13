from pathlib import Path

import click

from geomarc.pdf.watermark import apply_watermark
from geomarc.cli.common import common_watermark_options, resolve_custom_pattern, resolve_watermark_colors, console




@click.command()
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
@click.option(
    "--interval",
    "-i",
    type=click.IntRange(min=1),
    default=None,
    help="Apply watermark every Nth page.",
)
@common_watermark_options
def pdf(
    input_path: Path,
    output_path: Path,
    interval: int | None,
    complexity: str,
    pattern_file: Path | None,
    style: str,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protect: tuple[str, ...],
    color: str | None,
    colors: str | None,
) -> None:
    """Apply a geometric watermark to a PDF."""
    ctx = click.get_current_context()

    custom_points, custom_extra_lines, custom_polygons = (
            resolve_custom_pattern(ctx, pattern_file)
    )
    resolved_colors = resolve_watermark_colors(
        ctx=ctx,
        color=color,
        colors=colors,
    )

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
                style=style,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                interval=interval,
                protect=protect,
                custom_points=custom_points,
                custom_extra_lines=custom_extra_lines,
                custom_polygons=custom_polygons,
                colors=resolved_colors,
            )

    except (ValueError, FileNotFoundError) as error:
        raise click.ClickException(str(error)) from error

    console.print(
        f"[green]✓[/green] Watermark applied: "
        f"[bold]{output_path}[/bold]"
    )