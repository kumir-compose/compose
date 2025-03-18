from kumir_compose.packages.discover import Discoverer, WebPackage


class DependencyResolver:
    def __init__(self, discoverer: Discoverer) -> None:
        self.discoverer = discoverer
        self.resolving = set()

    def resolve_dependencies(self, package: WebPackage) -> list[WebPackage]:
        package = self.discoverer.get_package(package)
        dependencies = []
        self.resolving.add(package.full_name)
        for dependency_name, version in package.manifest.depends.items():
            dependency = WebPackage(dependency_name, version)
            if dependency.full_name in self.resolving:
                continue
            dependencies.extend(self.resolve_dependencies(dependency))
            dependencies.append(dependency)
        return dependencies
