from kumir_compose.commands.common import err_exit
from kumir_compose.config.config_file import ConfigModel
from kumir_compose.packages.exceptions import (
    FileNotFoundException, MalformedRemoteManifestException,
    NotFoundException, PackageAlreadyInstalledException,
)
from kumir_compose.packages.package_manager import PackageManager


def handle_errors(func):
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NotFoundException as exc:
            err_exit(
                f"Package {exc.resource} not found"
            )
        except MalformedRemoteManifestException as exc:
            err_exit(
                f"Package {exc.resource} has malformed manifest"
            )
        except FileNotFoundException as exc:
            err_exit(
                f"Package {exc.resource} tried to distribute "
                f"non-existent file {exc.file}"
            )
        except PackageAlreadyInstalledException as exc:
            err_exit(
                f"Package {exc.resource} is already installed"
            )
    return inner


@handle_errors
def depend(
        config: ConfigModel,
        name: str,
        version: str = "latest",
        update: bool = False
) -> None:
    config.project.depends[name] = version
    manager = PackageManager(config.project.library_location)
    if update:
        manager.update_package(name, version)
    else:
        manager.add_package(name, version)


@handle_errors
def undepend(
        config: ConfigModel,
        name: str
) -> None:
    if name in config.project.depends:
        config.project.depends.pop(name)
    manager = PackageManager(config.project.library_location)
    manager.remove_package(name)


@handle_errors
def install(config: ConfigModel, refresh: bool) -> None:
    manager = PackageManager(config.project.library_location)
    if refresh:
        manager.clean_packages()
    installed = manager.list_packages()
    for name, version in config.project.depends.items():
        if name not in installed:
            manager.add_package(name, version)
