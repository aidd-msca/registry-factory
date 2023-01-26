"""Registry factory module for a codebase."""
from typing import Any, Dict, List, Optional, Type

from registry_factory.index import IndexDict
from registry_factory.patterns.facade import ObserverFacade
from registry_factory.patterns.observer import RegistryObserver
from registry_factory.registration import AbstractRegistry
from registry_factory.tracker import Tracker


class Factory:
    """A factory class for creating registries."""

    @classmethod
    def create_registry(
        cls,
        shared: bool = False,
        checks: Optional[List[RegistryObserver]] = None,
    ) -> Type[AbstractRegistry]:
        class Registry(AbstractRegistry):
            facade = ObserverFacade(checks)
            index = IndexDict(shared=shared)
            arguments = IndexDict(shared=shared)

        return Registry

    @classmethod
    def view_called(cls) -> None:
        """View the accreditation information."""
        print("Called objects:")
        Tracker().show()

    @classmethod
    def get_subclass_choices(cls, choices: Dict[str, Dict]) -> Dict[str, Any]:
        """Return the choices for the subclass."""
        objects = {}

        RegistryClasses = AbstractRegistry.__subclasses__()
        registries = {reg.__name__.lower(): reg for reg in RegistryClasses}
        for name, selection in choices.items():
            for (registry, call) in selection.items():
                objects[name] = registries[registry].get_choice(call)

        return objects

    @classmethod
    def get_subclass_arguments(cls, argument_classes: Dict[str, Dict]) -> Dict[str, Any]:
        """Return the arguments for the subclass."""
        dataclasses = {}

        RegistryClasses = AbstractRegistry.__subclasses__()
        registries = {reg.__name__.lower(): reg for reg in RegistryClasses}
        for name, selection in argument_classes.items():
            for (registry, call) in selection.items():
                dataclasses[name] = registries[registry].get_arguments(call)

        return dataclasses
