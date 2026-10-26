from rich.console import Console
from rich.table import Table
from rich.markup import escape


def print_header(console: Console, title: str) -> None:
    console.print(f"[bold blue]{title}[/bold blue]")
    console.rule(style="blue")


def print_parameters(
    console: Console,
    parameters: dict[str, object],
) -> None:
    table = Table(show_header=False, pad_edge=False, box=None)

    table.add_column(style="bold", justify="left")
    table.add_column(justify="left")

    for name, value in parameters.items():
        if value is None:
            continue

        table.add_row(name, str(escape(str(value))))

    console.print(table)


def print_success(console: Console, message: str) -> None:
    console.print(f"[green]✓[/green] {escape(message)}")


def print_warning(console: Console, message: str) -> None:
    console.print(f"[yellow]![/yellow] {escape(message)}")


def print_error(console: Console, message: str) -> None:
    console.print(f"[red]✗[/red] {escape(message)}")


def print_processing_summary(
    console: Console,
    successful: int,
    failed: int,
    skipped: int | None = None,
) -> None:
    
    total = successful + failed + (skipped or 0)

    console.print()
    console.print("[bold]Processing complete[/bold]")

    console.print(f"Successful: [green]{successful}[/green]")
    console.print(f"Failed:     [red]{failed}[/red]")

    if skipped is not None:
        console.print(f"Skipped:    [yellow]{skipped}[/yellow]")

    console.print(f"Total:      [bold]{total}[/bold]")