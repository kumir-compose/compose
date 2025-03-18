import logging
import sys

import click

from kumir_compose.commands.compose import compose
from kumir_compose.commands.depend import depend, install, undepend
from kumir_compose.commands.run import run
from kumir_compose.config.config_file import load_config, save_config

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


@click.command()
@click.argument("filename")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading files"
)
@click.option(
    "--output", "-o",
    default=None,
    help="Output file name"
)
def kumir_compose(
        filename: str,
        encoding: str | None,
        output: str,
) -> None:
    """Compose .kum file."""
    config = load_config(encoding)
    compose(config, filename, encoding, output)


@click.group()
def kumir_compose_group():
    """Kumir-Compose CLI tool."""


@kumir_compose_group.command(name="depend")
@click.argument("name")
@click.option(
    "--version", "-v",
    default="latest",
    help="Package version"
)
@click.option(
    "--update", "-u",
    is_flag=True,
    default=False,
    help="Update or just install?"
)
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def depend_command(name: str, version: str, update: bool, encoding: str):
    """Install or update a dependency."""
    config = load_config(encoding)
    depend(config, name, version, update)
    save_config(config, encoding)


@kumir_compose_group.command(name="undepend")
@click.argument("name")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def undepend_command(name: str, encoding: str):
    """Remove a dependency."""
    config = load_config(encoding)
    undepend(config, name)
    save_config(config, encoding)


@kumir_compose_group.command(name="install")
@click.option(
    "--refresh", "-r",
    is_flag=True,
    default=False,
    help="Refresh or just fill in missing?"
)
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def install_command(refresh: bool, encoding: str):
    """Install all dependencies."""
    config = load_config(encoding)
    install(config, refresh)


@kumir_compose_group.command(name="run")
@click.argument("filename")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def install_command(filename: str, encoding: str):
    """Preprocess, compile and run Kumir2 file."""
    config = load_config(encoding)
    run(config, filename, encoding)


_SUBCOMMANDS = frozenset((
    "depend",
    "undepend",
    "install",
    "run",
    "debug",
))


def main():
    """Entrypoint."""
    if len(sys.argv) > 1 and sys.argv[1] not in _SUBCOMMANDS:
        kumir_compose()
    else:
        kumir_compose_group()
