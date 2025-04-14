from pathlib import Path

import yaml
from pydantic import BaseModel, field_validator


class WebModel(BaseModel):
    routes: dict[str, str]

    @property
    def beautiful_str(self) -> str:
        res = "routes:"
        for route, target in self.routes.items():
            res += f'\n  {route}: {target}'
        return res


def load_config(encoding: str | None = None) -> WebModel:
    contents = Path("kumir-compose-web.yml").read_text(encoding=encoding)
    yaml_obj = yaml.safe_load(contents)
    return WebModel(**yaml_obj)


def save_config(cfg: WebModel, encoding: str | None = None) -> None:
    obj = cfg.model_dump()
    yaml_str = yaml.safe_dump(
        obj,
        allow_unicode=True,
        indent=2
    )
    Path("kumir-compose-web.yml").write_text(yaml_str, encoding)


def save_beautify_config(
        cfg: WebModel,
        encoding: str | None = None
) -> None:
    Path("kumir-compose-yml.yml").write_text(cfg.beautiful_str, encoding)
