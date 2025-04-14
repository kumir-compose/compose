import os
import subprocess
import sys

import waitress

from kumir_compose.commands.common import err_exit
from kumir_compose.config.config_file import ConfigModel
from kumir_compose.web.config_file import WebModel
from kumir_compose.web.wsgi import create_compose_app


def web(
        config: ConfigModel,
        web_config: WebModel,
        encoding: str | None = None,
        bind_to: tuple[str, int] = ("0.0.0.0", 8000)
):
    """Command impl."""
    if config.settings.sdk.release is None:
        err_exit("Release SDK VM executable not set")
    app_class = create_compose_app(
        web_config.routes, config.settings.sdk.release
    )
    host, port = bind_to
    waitress.serve(app_class, host=host, port=port)
