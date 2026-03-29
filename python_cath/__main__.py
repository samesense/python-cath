# mypy: disable-error-code="attr-defined"

from typing import List

import typer
from python_cath import __version__
from python_cath.concat import concat
from rich.console import Console

app = typer.Typer(
    name="python-cath",
    help="Cat files w/ headers",
    add_completion=False,
    invoke_without_command=True,
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]python-cath[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command()
def main(
    file_list: List[str] = typer.Argument(...),
    output_file: str = typer.Option(..., "--output", "-o", help="Output file path"),
) -> None:
    """Concatenate CSV files with a shared header into output_file."""
    concat(file_list, output_file)
