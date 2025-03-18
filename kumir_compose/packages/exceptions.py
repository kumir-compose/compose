class PackageException(Exception):
    """Discover exception."""


class _ResourcedException(PackageException):
    def __init__(self, resource):
        self.resource = resource


class NotFoundException(_ResourcedException):
    """Not found."""


class MalformedRemoteManifestException(_ResourcedException):
    """Bad manifest."""


class FileNotFoundException(_ResourcedException):
    """Not found."""

    def __init__(self, resource: str, file: str) -> None:
        super().__init__(resource)
        self.file = file


class PackageAlreadyInstalledException(_ResourcedException):
    """Package already installed."""
