from pathlib import Path

import yaml
from pydantic import BaseModel


class ProjectModel(BaseModel):
    name: str
    depends: dict[str, str] = {}
    library_location: str = "lib"
    lookup: list[str] = ["lib"]
    filename_format: str = "%s.kum"
    distribute: list[str] = []


class SDKModel(BaseModel):
    compiler: str | None = None
    debug: str | None = None
    release: str | None = None


class ComposeModel(BaseModel):
    sdk: SDKModel


class ConfigModel(BaseModel):
    project: ProjectModel
    settings: ComposeModel | None = None


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
    Path("kumir-compose.yml").write_text(yaml_str)
