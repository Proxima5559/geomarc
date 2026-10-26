from pathlib import Path
import click
from rich.console import Console

from geomarc.cli.errors import handle_cli_errors
from geomarc.image.folder import process_folder
from geomarc.cli.common import (
    common_watermark_options,
    parse_protected_regions,
    resolve_custom_pattern,
    resolve_watermark_options,
)
from geomarc.cli.formater import (  
    print_header, 
    print_parameters, 
    print_success, 
    print_processing_summary
)


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
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Process images in all subfolders recursively.",
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
    recursive: bool,
    on_unsupported: str, 
    complexity: str,
    pattern_file: Path | None,
    style: str | None,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protect: tuple[str, ...],

) -> None:
    """Apply a geometric watermark to all images in a folder."""
    ctx = click.get_current_context()
    complexity, line_width, opacity, count = resolve_watermark_options(
        ctx, complexity, line_width, opacity, count
    )
    custom_points, custom_extra_lines, custom_polygons = (
            resolve_custom_pattern(ctx, pattern_file)
    )

    if output_dir.resolve() == input_dir.resolve():
        raise click.UsageError(
            "Input and output directories must be different."
        )

    protected_regions = parse_protected_regions(protect)   
  
    with handle_cli_errors():
        print_header(console, "GEOMARC|FOLDERS")

        print_parameters(
            console,
            {
                "Input directory": input_dir,
                "Output directory": output_dir,
                "Recursive": recursive,
                "Unsupported files": on_unsupported.lower(),
                "Complexity": complexity.lower(),
                "Style": style,
                "Line width": line_width,
                "Opacity": opacity,
                "Seed": seed,
                "Watermarks": count,
                "Protected regions": len(protected_regions),
                "Custom pattern": pattern_file,
            },
        )

        with console.status("[bold]Processing folder..."):
            processed, skipped = process_folder(
                input_dir=input_dir,
                output_dir=output_dir,
                recursive=recursive,
                complexity=complexity.lower(),
                on_unsupported=on_unsupported.lower(),
                style=style,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                protected_regions=protected_regions,
                custom_points=custom_points,
                custom_extra_lines=custom_extra_lines,
                custom_polygons=custom_polygons,
            )

    print_processing_summary(
        console,
        successful=processed,
        failed=0,
        skipped=skipped,
    )

    print_success(console, f"Results saved to: {output_dir}")