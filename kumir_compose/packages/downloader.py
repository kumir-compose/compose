from pathlib import Path

from kumir_compose.packages.discover import Discoverer, WebPackage


class Downloader:
    def __init__(
            self,
            discoverer: Discoverer,
            download_dir: str
    ) -> None:
        self.discoverer = discoverer
        self.root = download_dir

    def download_package(self, package: WebPackage) -> None:
        pkg_name = package.name.split("/")[-1]
        for filename in package.manifest.distribute:
            contents = self.discoverer.get_file_in_repo(package, filename)
            path = Path(self.root, pkg_name, filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
