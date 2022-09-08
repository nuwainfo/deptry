import logging
from typing import List

from deptry.dependency import Dependency
from deptry.issue_finders.issue_finder import IssueFinder
from deptry.module import Module


class TransitiveDependenciesFinder(IssueFinder):
    """
    Given a list of imported modules and a list of project dependencies, determine which ones are transitive.
    """

    def __init__(
        self, imported_modules: List[Module], dependencies: List[Dependency], list_to_ignore: List[str] = []
    ) -> None:
        super().__init__(imported_modules, dependencies, list_to_ignore)

    def find(self) -> List[str]:
        logging.debug("\nScanning for transitive dependencies...")
        transitive_dependencies = []
        for module in self.imported_modules:
            logging.debug(f"Scanning module {module.name}...")
            if self._is_transitive(module):
                transitive_dependencies.append(module.package)
        return transitive_dependencies

    def _is_transitive(self, module: Module) -> bool:
        if (
            module.package is not None
            and not self._module_in_any_top_level(module)
            and not self._module_in_dependencies(module)
            and not module.is_local_module()
        ):
            if module.name in self.list_to_ignore:
                logging.debug(f"Module '{module.package}' found to be a transitive dependency, but ignoring.")
            else:
                logging.debug(f"Dependency '{module.package}' marked as a transitive dependency.")
                return True
        return False
