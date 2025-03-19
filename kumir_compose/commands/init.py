import os
import sys
from pathlib import Path

import click
from alive_progress import alive_bar

from kumir_compose.commands.common import err_exit
from kumir_compose.config.config_file import (
    ComposeModel,
    ConfigModel,
    ProjectModel,
    SDKModel,
    save_beautify_config,
)


def init():
    """Command impl."""
    if Path("kumir-compose.yml").exists():
        err_exit("kumir-compose.yml already exists here.")
    project_name = click.termui.prompt("Enter project name")
    lib_location = click.termui.prompt(
        "Select library directory", default="lib", show_default=True
    )
    project_conf = ProjectModel(
        name=project_name, library_location=lib_location
    )
    kumir2_bc = None
    kumir2_xrun = None
    if sys.platform == "win32":
        should_scan = click.termui.confirm(
            "Do you want Kumir-Compose to automatically find Kumir SDK",
            prompt_suffix="? ",
            default=True,
            show_default=True
        )
        if should_scan:
            with alive_bar(monitor=None, stats=None, title="Scanning"):
                kumir2_bc, kumir2_xrun = _scan_windows_kumir_sdk()
    if not kumir2_bc or not kumir2_xrun:
        kumir2_bc = click.termui.prompt(
            "Enter path to kumir2-bc",
            default=kumir2_bc,
            show_default=True
        )
        kumir2_xrun = click.termui.prompt(
            "Enter path to kumir2-xrun",
            default=kumir2_xrun,
            show_default=True
        )
    settings_conf = ComposeModel(
        sdk=SDKModel(
            debug=kumir2_xrun,
            release=kumir2_xrun,
            compiler=kumir2_bc
        )
    )
    cfg = ConfigModel(project=project_conf, settings=settings_conf)
    save_beautify_config(cfg)
    click.termui.echo(click.style("Config created.", fg="green"), color=True)

def _scan_windows_kumir_sdk():
    kumir2_bc = None
    kumir2_xrun = None
    for win_root in [r"C:\Program Files (x86)", r"C:\Program Files"]:
        for root, dirs, files in os.walk(win_root):
            for file in files:
                if file == "kumir2-bc.exe":
                    kumir2_bc = os.path.join(root, file)
                if file == "kumir2-xrun.exe":
                    kumir2_xrun = os.path.join(root, file)
    return kumir2_bc, kumir2_xrun
