import os
import subprocess
import sys

from kumir_compose.commands.common import err_exit
from kumir_compose.commands.compose import compose
from kumir_compose.config.config_file import ConfigModel


def compile_(
        config: ConfigModel,
        name: str,
        encoding: str,
        output_file: str | None = None
) -> None:
    """Command impl."""
    if config.settings.sdk.compiler is None:
        err_exit("Release SDK compiler not set")
    output_name = f"{name}.assembled.kum"
    origin_output = f"{name}.assembled.kod"
    compose(config, name, encoding, output_name)
    proc = subprocess.run(
        [config.settings.sdk.compiler, output_name],
        stdout=sys.stdout,
        stderr=sys.stderr, check=False
    )
    os.remove(output_name)
    output_file = output_file or (name.removesuffix(".kum") + ".kod")
    if os.path.exists(output_file):
        os.remove(output_file)
    os.rename(origin_output, output_file)
    if proc.returncode != 0:
        err_exit(f"Process failed to finish with exit code {proc.returncode}")
