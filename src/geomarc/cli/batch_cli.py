from pathlib import Path
import click

from geomarc.cli.errors import handle_cli_errors
from geomarc.image.watermark import apply_watermark_batch
from .common import (
    common_watermark_options,
    parse_protected_regions,
    resolve_custom_pattern,
    resolve_watermark_options,
    get_effective_option,
)



@click.command(name="batch")
@click.argument(
    "inputs",
    nargs=-1,
    type=click.Path(exists=True, path_type=Path),
    required=True,
)
@click.option(
    "-d",
    "--output-dir",
    required=True,
    type=click.Path(path_type=Path),
    help="Output directory for processed images.",
)
@common_watermark_options
@click.pass_context
def batch(
    ctx: click.Context,
    inputs: tuple[Path, ...],
    output_dir: Path,
    complexity: str,
    style: str | None,
    pattern_file: Path | None,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protect: tuple[str, ...],
) -> None:
    """Process multiple specified files with watermarks."""
    resolved_complexity, resolved_line_width, resolved_opacity, resolved_count = (
        resolve_watermark_options(ctx, complexity, line_width, opacity, count)
    )
    resolved_style = get_effective_option(ctx, "style", style, None)
    resolved_seed = get_effective_option(ctx, "seed", seed, None)
    protected_regions = parse_protected_regions(protect) if protect else None

    custom_points, custom_extra_lines, custom_polygons = (
            resolve_custom_pattern(ctx, pattern_file)
     )
    
    with handle_cli_errors():
        results = apply_watermark_batch(
            inputs=inputs,
            output_dir=output_dir,
            complexity=resolved_complexity,
            style=resolved_style,
            line_width=resolved_line_width,
            opacity=resolved_opacity,
            seed=resolved_seed,
            count=resolved_count,
            protected_regions=protected_regions,
            custom_points=custom_points,
            custom_extra_lines=custom_extra_lines,
            custom_polygons=custom_polygons,
        )

    click.echo("Batch processing\n")
    processed_count = 0
    failed_count = 0

    for res in results:
        if res.success:
            click.echo(f"✓ {res.input_path.name} → {res.output_path}")
            processed_count += 1
        else:
            click.echo(f"✗ {res.input_path.name} — {res.error}")
            failed_count += 1

    click.echo("\nSummary")
    click.echo(f"  Processed: {processed_count}")
    click.echo(f"  Failed:    {failed_count}")