from contextlib import contextmanager
import click
from rich.console import Console

error_console = Console(stderr=True)

def print_cli_error(message: str) -> None:
    error_console.print(f"[red]✗[/red] {message}")

@contextmanager
def handle_cli_errors():
    try:
        yield
    except (click.BadParameter, click.UsageError, click.ClickException):
        raise
    except FileNotFoundError as error:
        message = (
            f"File or directory not found: "
            f"{error.filename or error}"
        )
        print_cli_error(message)
        raise click.ClickException(message) from error

    except NotADirectoryError as error:
        message = f"Path is not a directory: {error}"
        print_cli_error(message)
        raise click.ClickException(message) from error

    except PermissionError as error:
        message = f"Permission denied: {error}"
        print_cli_error(message)
        raise click.ClickException(message) from error

    except ValueError as error:
        message = str(error)
        print_cli_error(message)
        raise click.ClickException(message) from error

    except OSError as error:
        message = f"System or I/O error occurred: {error}"
        print_cli_error(message)
        raise click.ClickException(message) from error