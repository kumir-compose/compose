import shutil
from pathlib import Path

from kumir_compose.packages.discover import WebPackage


class DiskPackageManager:
    def __init__(self, root: str) -> None:
        self.root = root

    def clean_root(self) -> None:
        if Path(self.root).exists():
            shutil.rmtree(self.root)

    def clean_package(self, package_name) -> None:
        pkg_name = package_name.split("/")[-1]
        if Path(self.root, pkg_name).exists():
            shutil.rmtree(str(Path(self.root, pkg_name)))
