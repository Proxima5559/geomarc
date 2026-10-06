from contextlib import contextmanager
import click


@contextmanager
def handle_cli_errors():
    try:
        yield
    except (click.BadParameter, click.UsageError, click.ClickException):
        raise
    except FileNotFoundError as error:
        raise click.ClickException(f"File or directory not found: {error.filename or error}") from error
    except NotADirectoryError as error:
        raise click.ClickException(f"Path is not a directory: {error}") from error
    except PermissionError as error:
        raise click.ClickException(f"Permission denied: {error}") from error
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    except OSError as error:
        raise click.ClickException(f"System or I/O error occurred: {error}") from error