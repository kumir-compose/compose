from pathlib import Path

import click
from unicodedata import lookup

from kumir_compose.preprocessor.exceptions import PositionedException
from kumir_compose.preprocessor.lexer import scan_file
from kumir_compose.preprocessor.preprocessor import Preprocessor


@click.command()
@click.argument("filename")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading files"
)
@click.option(
    "--lookup", "-l",
    default=["", "lib"],
    help="Where to look for inclusion files",
    multiple=True
)
@click.option(
    "--filename-format", "-f",
    default="%s.kum",
    help="Output file name format"
)
def kumir_compose(
        filename: str,
        encoding: str | None,
        lookup: list[str],
        filename_format: str
) -> None:
    """Compose .kum file."""
    file = Path(filename)
    if not file.exists() or not file.is_file():
        _err("File not found")
    try:
        tokens = scan_file(filename, encoding)
        source = file.read_text(encoding=encoding)
        preprocessor = Preprocessor(
            filename,
            source,
            tokens,
            encoding=encoding,
            lookup_paths=lookup
        )
        source = preprocessor.process()
        Path(filename_format % (filename,)).write_text(
            source,
            encoding="UTF-8-sig"
        )
    except PositionedException as exc:
        _err(str(exc))


def _err(text: str) -> None:
    click.echo(
        click.style(text, fg="red"),
        err=True,
        color=True
    )
    raise click.exceptions.Exit(1)


def main():
    """Entrypoint."""
    kumir_compose()
