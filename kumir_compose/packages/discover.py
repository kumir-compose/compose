from dataclasses import dataclass

import pydantic
import requests
import yaml
from github import Github

from kumir_compose.config.config_file import ConfigModel, ProjectModel
from kumir_compose.packages.exceptions import (
    FileNotFoundException,
    MalformedRemoteManifestException,
    NotFoundException,
)


@dataclass
class WebPackage:
    name: str
    version: str
    manifest: ProjectModel | None = None
    url: str | None = None

    @property
    def full_name(self) -> str:
        return f"{self.name}:{self.version}"


class Discoverer:
    def __init__(self):
        self.gh = Github()

    def get_package(self, package: WebPackage) -> WebPackage:
        manifest = self._get_manifest_text(package)
        try:
            yaml_obj = yaml.safe_load(manifest)
            manifest_obj = ConfigModel(**yaml_obj)
            package.manifest = manifest_obj.project
            return package
        except yaml.YAMLError:
            raise MalformedRemoteManifestException(package.full_name)
        except pydantic.ValidationError as exc:
            raise MalformedRemoteManifestException(package.full_name) from exc

    def _get_repo_of_pkg(self, package: WebPackage) -> str:
        pkg_name = package.name
        version = package.version
        if version == "latest":
            version = "master"
        if "/" not in package.name:
            pkg_name = f"kumir-compose/{package.name}"
        return (
            f"https://raw.githubusercontent.com/{pkg_name}/{version}"
        )

    def _get_manifest_text(self, package: WebPackage) -> str:
        repo = self._get_repo_of_pkg(package)
        response = requests.get(f"{repo}/kumir-compose.yml")
        if response.status_code != 200:
            raise NotFoundException(package.full_name)
        return response.text

    def get_file_in_repo(self, package: WebPackage, filename: str) -> bytes:
        repo = self._get_repo_of_pkg(package)
        response = requests.get(f"{repo}/{filename}")
        if response.status_code != 200:
            raise FileNotFoundException(package.full_name, filename)
        return response.content
