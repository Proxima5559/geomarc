from collections.abc import Sequence

from rich.console import Console
from rich.table import Table

from geomarc.generator.placement import Placement


def show_inspection(
    console: Console,
    *,
    image_width: int,
    image_height: int,
    image_format: str | None,
    complexity: str,
    style: str | None,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    placements: Sequence[Placement],
) -> None:


    console.print("[bold cyan]Image[/bold cyan]")
    console.print(f"Size: {image_width} × {image_height}")
    console.print(f"Format: {image_format or 'unknown'}")
    console.print()

    console.print("[bold cyan]Watermark configuration[/bold cyan]")
    console.print(f"Count: {count}")
    console.print(f"Complexity: {complexity}")
    console.print(f"Style: {style or 'auto'}")
    console.print(f"Opacity: {opacity}")
    console.print(f"Line width: {line_width}")
    console.print(f"Seed: {seed if seed is not None else 'random'}")
    console.print()

    table = Table(title="Placements")

    table.add_column("#", justify="right")
    table.add_column("X", justify="right")
    table.add_column("Y", justify="right")
    table.add_column("Size", justify="right")
    table.add_column("Rotation", justify="right")

    for index, placement in enumerate(placements, start=1):
        table.add_row(
            str(index),
            str(round(placement.x)),
            str(round(placement.y)),
            (
                f"{round(placement.width)}×"
                f"{round(placement.height)}"
            ),
            f"{placement.rotation:.1f}°",
        )

    console.print(table)