import click
from geomarc.config import load_config
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

def get_effective_option(
    ctx: click.Context | None, param_name: str, cli_value, default_value
):
    if (
        ctx
        and ctx.get_parameter_source(param_name)
        == click.ParameterSource.COMMANDLINE
    ):
        return cli_value
    config = load_config()
    if param_name in config and config[param_name] is not None:
        return config[param_name]
    return default_value

def resolve_watermark_options(
    ctx: click.Context,
    complexity: str,
    line_width: float,
    opacity: int,
    count: int,
) -> tuple[str, float, int, int]:
    return (
        get_effective_option(ctx, "complexity", complexity, "medium"),
        get_effective_option(ctx, "line_width", line_width, 2.0),
        get_effective_option(ctx, "opacity", opacity, 100),
        get_effective_option(ctx, "count", count, 5),
    )

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
        click.option(
            "--inspect",
            is_flag=True,
            default=False,
            help=(
                "Show the generated watermark placements "
                "without creating the output file."
            ),
        ),
    ]

    for option in reversed(options):
        func = option(func)

    return func