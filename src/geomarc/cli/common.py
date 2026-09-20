import click

def common_watermark_options(func):
    options = [
        click.option(
            "--complexity",
            "-c",
            type=click.Choice(["low", "medium", "high"], case_sensitive=False),
            default="medium",
            show_default=True,
            help="Complexity of the generated pattern.",
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
    ]
    for option in reversed(options):
        func = option(func)
    return func