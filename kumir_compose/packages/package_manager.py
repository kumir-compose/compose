import logging
import os
from pathlib import Path

from kumir_compose.packages.discover import Discoverer, WebPackage
from kumir_compose.packages.disk_manager import DiskPackageManager
from kumir_compose.packages.downloader import Downloader
from kumir_compose.packages.exceptions import PackageAlreadyInstalledException
from kumir_compose.packages.resolver import DependencyResolver


class PackageManager:
    def __init__(self, root: str) -> None:
        self.root = root
        self.discoverer = Discoverer()
        self.resolver = DependencyResolver(self.discoverer)
        self.downloader = Downloader(self.discoverer, root)
        self.disk_mgr = DiskPackageManager(root)

    def list_packages(self) -> list[str]:
        if Path(self.root).exists():
            return os.listdir(self.root)
        return []

    def remove_package(self, name: str) -> None:
        self.disk_mgr.clean_package(name)
        logging.info("Removed package")

    def add_package(self, name: str, version: str) -> None:
        if name.split("/")[-1] in self.list_packages():
            raise PackageAlreadyInstalledException(name)
        logging.info("Resolving package...")
        package = WebPackage(name, version)
        package = self.discoverer.get_package(package)
        logging.info("Resolving dependencies...")
        dependencies = self.resolver.resolve_dependencies(package)
        logging.info("Downloading dependencies...")
        for dependency in dependencies:
            if dependency.name.split("/")[-1] not in self.list_packages():
                self.downloader.download_package(dependency)
        logging.info("Downloading package...")
        self.downloader.download_package(package)
        logging.info("Added")

    def update_package(self, name: str, version: str) -> None:
        self.remove_package(name)
        self.add_package(name, version)

    def clean_packages(self):
        self.disk_mgr.clean_root()
