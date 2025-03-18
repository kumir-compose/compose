import os
import subprocess
import sys

from kumir_compose.commands.common import err_exit
from kumir_compose.commands.compose import compose
from kumir_compose.config.config_file import ConfigModel


def run(
        config: ConfigModel,
        name: str,
        encoding: str
) -> None:
    if config.settings.sdk.release is None:
        err_exit("Release SDK VM executable not set")
    if config.settings.sdk.compiler is None:
        err_exit("Release SDK compiler not set")
    output_name = f"{name}.assembled.kum"
    compiled_name = f"{name}.assembled.kod"
    compose(config, name, encoding, output_name)
    subprocess.run(
        [config.settings.sdk.compiler, output_name],
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    proc = subprocess.run(
        [config.settings.sdk.release, compiled_name],
        stdout=sys.stdout,
        stderr=sys.stderr,
        stdin=sys.stdin,
    )
    os.remove(output_name)
    os.remove(compiled_name)
    if proc.returncode != 0:
        err_exit(f"Process failed to finish with exit code {proc.returncode}")
