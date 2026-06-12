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
    files: List[str] = typer.Argument(
        ...,
        help="Two or more input files followed by the output file "
        "(the last argument is the output).",
    ),
) -> None:
    """Concatenate CSV files with a shared header.

    Provide two or more input files followed by the output file as the
    final argument, e.g. ``python-cath in1 in2 out``.
    """
    if len(files) < 3:
        console.print(
            "[red]Error:[/] need at least two input files plus an output "
            "file; the last argument is the output and would otherwise "
            "overwrite an input.",
        )
        raise typer.Exit(code=2)
    *input_files, output_file = files
    concat(input_files, output_file)


if __name__ == "__main__":
    app()
