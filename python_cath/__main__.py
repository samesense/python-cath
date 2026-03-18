# mypy: disable-error-code="attr-defined"

from typing import List, Optional

import random
from enum import Enum

import typer
from python_cath import __version__
from python_cath.concat import concat
from python_cath.example import hello
from rich.console import Console

app = typer.Typer(
    name="python-cath",
    help="Cat files w/ headers",
    add_completion=False,
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
    output_file: str = typer.Argument(...),
) -> None:
    """Prints a greeting for a giving name."""
    concat(file_list, output_file)
