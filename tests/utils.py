from pathlib import Path


def read_fix_file(filename: str) -> str:
    """Read fixture file."""
    return Path("tests", "fixtures", filename).read_text(encoding="UTF-8")
