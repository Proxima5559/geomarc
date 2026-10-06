import click
from geomarc.generator.placement import ProtectedRegion

def parse_protected_regions(
    values: tuple[str, ...],
) -> list[ProtectedRegion]:
    regions = []

    for value in values:
        parts = value.split(",")

        if len(parts) != 4:
            raise click.BadParameter(
                "Protected region must have "
                "4 values: left,top,right,bottom"
            )

        try:
            left, top, right, bottom = (
                float(part.strip())
                for part in parts
            )
        except ValueError as error:
            raise click.BadParameter(
                "Protected region coordinates "
                "must be numbers"
            ) from error

        try:
            region = ProtectedRegion(
                left=left,
                top=top,
                right=right,
                bottom=bottom,
            )
        except ValueError as error:
            raise click.BadParameter(
                str(error),
                param_hint="--protect"
            ) from error

        regions.append(region)

    return regions


def common_watermark_options(func):

    options = [

        click.option(
            "--complexity",
            "-c",
            type=click.Choice(
                ["low", "medium", "high"],
                case_sensitive=False,
            ),
            default="medium",
            show_default=True,
            help="Complexity of the generated pattern.",
        ),
        click.option(
            "--style",
            "-st",
            type=click.Choice(
                [
                    "line_mesh",
                    "polygon_network",
                    "angular_sharp",
                    "minimal",
                    "dense_geometric",
                ],
                case_sensitive=False,
            ),
            default=None,
            show_default=True,
            help="Geometric style of the watermark pattern.",
        ),

        click.option(
            "--line-width",
            "-w",
            type=click.FloatRange(min=0.1),
            default=2.0,
            show_default=True,
            help="Width of watermark lines.",
        ),

        click.option(
            "--opacity",
            "-o",
            type=click.IntRange(min=0, max=255),
            default=100,
            show_default=True,
            help="Watermark opacity.",
        ),

        click.option(
            "--seed",
            "-s",
            type=int,
            default=None,
            help="Seed used to generate a deterministic pattern.",
        ),

        click.option(
            "--count",
            "-n",
            type=click.IntRange(min=3, max=10),
            default=5,
            show_default=True,
            help="Number of watermark patterns to generate.",
        ),

        click.option(
            "--protect",
            "-p",
            multiple=True,
            type=str,
            help=(
                "Protected region in the form "
                "left,top,right,bottom. "
                "Can be specified multiple times."
            ),
        ),
    ]

    for option in reversed(options):
        func = option(func)

    return func