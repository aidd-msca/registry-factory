"""Registraty factory module for a codebase."""
from typing import Any, Dict, List, Optional, Type

from abstract_codebase.index import IndexDict
from abstract_codebase.patterns.facade import ObserverFacade
from abstract_codebase.patterns.observer import RegistryObserver
from abstract_codebase.registration import AbstractRegistry
from abstract_codebase.tracker import Tracker


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
            index = IndexDict(shared=shared)  # SharedIndexDict() if shared else IndexDict()
            arguments = IndexDict(shared=shared)  # SharedIndexDict() if shared else IndexDict()

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
