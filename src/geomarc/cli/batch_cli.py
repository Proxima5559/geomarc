from pathlib import Path
import click
from rich.console import Console

from geomarc.cli.errors import handle_cli_errors
from geomarc.image.watermark import apply_watermark_batch
from .common import (
    common_watermark_options,
    parse_protected_regions,
    resolve_custom_pattern,
    resolve_watermark_options,
    get_effective_option,
)

from geomarc.cli.formater import (  
    print_header, 
    print_parameters, 
    print_success, 
    print_error,
    print_processing_summary
)

console = Console()

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
        print_header(console, "GEOMARC|BATCH")

        print_parameters(
            console,
            {
                "Input files": len(inputs),
                "Output directory": output_dir,
                "Complexity": resolved_complexity.lower(),
                "Style": resolved_style,
                "Line width": resolved_line_width,
                "Opacity": resolved_opacity,
                "Seed": resolved_seed,
                "Watermarks": resolved_count,
                "Protected regions": (
                    len(protected_regions) if protected_regions else 0
                ),
                "Custom pattern": pattern_file,
            },
        )

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

    console.print()

    for result in results:
        if result.success:
            print_success(
                console,
                f"{result.input_path.name} → {result.output_path}",
            )
            successful_count += 1
        else:
            print_error(
                console,
                f"{result.input_path.name} — {result.error}",
            )
            failed_count += 1

    print_processing_summary(
        console,
        successful=successful_count,
        failed=failed_count,
    )