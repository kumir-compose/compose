from pathlib import Path

from kumir_compose.commands.common import err_exit
from kumir_compose.config.config_file import ConfigModel
from kumir_compose.preprocessor.exceptions import PositionedException
from kumir_compose.preprocessor.lexer import scan_file
from kumir_compose.preprocessor.preprocessor import Preprocessor


def compose(
        config: ConfigModel,
        filename: str,
        encoding: str | None,
        output_name: str | None = None
) -> None:
    file = Path(filename)
    if not output_name:
        output_name = config.project.filename_format % (filename,)
    if not file.exists() or not file.is_file():
        err_exit("File not found")
    try:
        tokens = scan_file(filename, encoding)
        source = file.read_text(encoding=encoding)
        preprocessor = Preprocessor(
            filename,
            source,
            tokens,
            encoding=encoding,
            lookup_paths=config.project.lookup
        )
        source = preprocessor.process()
        Path(output_name).write_text(source, encoding="UTF-8-sig")
    except PositionedException as exc:
        err_exit(str(exc))
