import textwrap
from pathlib import Path
from typing import Final

import yaml
from pydantic import BaseModel

_DEFAULT_LIB_LOC: Final = "lib"
_DEFAULT_FILENAME_FMT: Final = "%s.kum"


class ProjectModel(BaseModel):
    name: str
    depends: dict[str, str] = {}
    library_location: str = _DEFAULT_LIB_LOC
    lookup: list[str] = [_DEFAULT_LIB_LOC]
    filename_format: str = _DEFAULT_FILENAME_FMT
    distribute: list[str] = []
    kpsi_support: bool = False

    @property
    def beautiful_str(self) -> str:
        res = f"name: {self.name}"
        if self.kpsi_support:
            res += "\nkpsi_support: true"
        if self.depends:
            res += "\ndepends:"
            for dep_name, dep_version in self.depends.items():
                res += f"\n  {dep_name}: {dep_version}"
        if self.library_location != _DEFAULT_LIB_LOC:
            res += f'\nlibrary_location: "{self.library_location!r}"'
        if self.lookup != [_DEFAULT_LIB_LOC]:
            res += "\nlookup:"
            for loc in self.lookup:
                res += f'\n  - "{loc!r}"'
        if self.filename_format != _DEFAULT_FILENAME_FMT:
            res += f'\nfilename_format: "{self.filename_format!r}"'
        if self.distribute:
            res += "\ndistribute:"
            for loc in self.distribute:
                res += f'\n  - "{loc!r}"'
        return res


class SDKModel(BaseModel):
    compiler: str | None = None
    debug: str | None = None
    release: str | None = None


class ComposeModel(BaseModel):
    sdk: SDKModel

    @property
    def beautiful_str(self) -> str:
        return (
            f"sdk:\n"
            f"  compiler: {self.sdk.compiler!r}\n"
            f"  release: {self.sdk.release!r}\n"
            f"  debug: {self.sdk.debug!r}\n"
        )


class ConfigModel(BaseModel):
    project: ProjectModel
    settings: ComposeModel | None = None

    @property
    def beautiful_str(self) -> str:
        project = textwrap.indent(self.project.beautiful_str, "  ")
        settings = ""
        if self.settings:
            settings = textwrap.indent(self.settings.beautiful_str, "  ")
        return (
            f"project:\n"
            f"{project}\n\n\n"
            f"settings:\n"
            f"{settings}"
        )


def load_config(encoding: str | None = None) -> ConfigModel:
    contents = Path("kumir-compose.yml").read_text(encoding=encoding)
    yaml_obj = yaml.safe_load(contents)
    return ConfigModel(**yaml_obj)


def save_config(cfg: ConfigModel, encoding: str | None = None) -> None:
    obj = cfg.model_dump()
    yaml_str = yaml.safe_dump(
        obj,
        allow_unicode=True,
        indent=2
    )
    Path("kumir-compose.yml").write_text(yaml_str, encoding)


def save_beautify_config(
        cfg: ConfigModel,
        encoding: str | None = None
) -> None:
    Path("kumir-compose.yml").write_text(cfg.beautiful_str, encoding)
