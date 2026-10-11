import click
from rich.console import Console

from geomarc.cli.errors import handle_cli_errors
from geomarc.config import (
    load_config,
    set_config_value,
    reset_config,
    VALID_KEYS,
)

console = Console()


@click.group()
def config() -> None:
    """Manage user configuration settings."""
    pass


@config.command()
def show() -> None:
    """Show current user configuration."""
    with handle_cli_errors():
        cfg = load_config()
        if not cfg:
            console.print("[dim]No custom configuration set.[/dim]")
            return
        console.print("[bold cyan]Current configuration:[/bold cyan]")
        for key, value in sorted(cfg.items()):
            console.print(f"  {key}: [bold]{value}[/bold]")


@config.command()
@click.argument(
    "key",
    type=click.Choice(list(VALID_KEYS), case_sensitive=False),
)
@click.argument("value", type=str)
def set(key: str, value: str) -> None:
    """Set a configuration value."""
    key = key.lower()
    with handle_cli_errors():
        parsed_value = validate_config_value(key, value)
        set_config_value(key, parsed_value)
        console.print(
            f"[green]✓[/green] Set [bold]{key}[/bold] to [bold]{parsed_value}[/bold]"
        )


@config.command()
def reset() -> None:
    """Reset configuration to default values."""
    with handle_cli_errors():
        reset_config()
        console.print("[green]✓[/green] Configuration reset to defaults.")


def validate_config_value(key: str, value: str):
    if key == "complexity":
        val = value.lower()
        if val not in ("low", "medium", "high"):
            raise click.BadParameter("Complexity must be low, medium, or high.")
        return val
    elif key == "count":
        try:
            val = int(value)
        except ValueError as err:
            raise click.BadParameter("Count must be an integer.") from err
        if not (3 <= val <= 10):
            raise click.BadParameter("Count must be between 3 and 10.")
        return val
    elif key == "opacity":
        try:
            val = int(value)
        except ValueError as err:
            raise click.BadParameter("Opacity must be an integer.") from err
        if not (0 <= val <= 255):
            raise click.BadParameter("Opacity must be between 0 and 255.")
        return val
    elif key == "line_width":
        try:
            val = float(value)
        except ValueError as err:
            raise click.BadParameter("Line width must be a number.") from err
        if val < 0.1:
            raise click.BadParameter("Line width must be at least 0.1.")
        return val
    return value