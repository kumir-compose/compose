import logging
import sys
from pathlib import Path

import click

from kumir_compose.commands.common import err_exit
from kumir_compose.commands.compile import compile_
from kumir_compose.commands.compose import compose
from kumir_compose.commands.depend import depend, install, undepend
from kumir_compose.commands.init import init
from kumir_compose.commands.run import run
from kumir_compose.commands.web import web
from kumir_compose.config.config_file import (
    load_config,
    save_beautify_config,
)
from kumir_compose.web import config_file as web_config

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
    _guard_config_exists()
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
    _guard_config_exists()
    config = load_config(encoding)
    depend(config, name, version, update)
    save_beautify_config(config, encoding)


@kumir_compose_group.command(name="undepend")
@click.argument("name")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def undepend_command(name: str, encoding: str):
    """Remove a dependency."""
    _guard_config_exists()
    config = load_config(encoding)
    undepend(config, name)
    save_beautify_config(config, encoding)


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
    _guard_config_exists()
    config = load_config(encoding)
    install(config, refresh)


@kumir_compose_group.command(name="run")
@click.argument("filename")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def run_command(filename: str, encoding: str):
    """Preprocess, compile and run Kumir2 file."""
    _guard_config_exists()
    config = load_config(encoding)
    run(config, filename, encoding)


@kumir_compose_group.command(name="init")
def init_command():
    """Init Kumir-Compose project."""
    init()


@kumir_compose_group.command(name="compile")
@click.argument("filename")
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
@click.option(
    "--output", "-o",
    default=None,
    help="Name of output file"
)
def compile_command(filename: str, encoding: str, output: str):
    """Preprocess and compile Kumir2 file."""
    _guard_config_exists()
    config = load_config(encoding)
    compile_(config, filename, encoding, output)


@kumir_compose_group.command(name="web")
@click.option(
    "--bind", "-b",
    default="0.0.0.0:8000",
    help="IP:port to bind to"
)
@click.option(
    "--encoding", "-e",
    default="UTF-8",
    help="What encoding to use when reading config"
)
def web_command(encoding: str, bind: str):
    """Run web server."""
    _guard_config_exists()
    _guard_web_config_exists()
    config = load_config(encoding)
    web_conf = web_config.load_config(encoding)
    bind_addr, bind_port = bind.split(":", maxsplit=1)
    web(config, web_conf, encoding, (bind_addr, int(bind_port)))


_SUBCOMMANDS = frozenset((
    "depend",
    "undepend",
    "install",
    "run",
    "debug",
    "init",
    "compile",
    "web"
))


def main():
    """Entrypoint."""
    if len(sys.argv) > 1 and sys.argv[1] not in _SUBCOMMANDS:
        kumir_compose()
    else:
        kumir_compose_group()


def _guard_config_exists():
    if not Path("kumir-compose.yml").exists():
        err_exit(
            "kumir-compose.yml not found in cwd.\n"
            "Run `kumir-compose init` to create one"
        )


def _guard_web_config_exists():
    if not Path("kumir-compose-web.yml").exists():
        err_exit(
            "kumir-compose-web.yml not found in cwd."
        )
