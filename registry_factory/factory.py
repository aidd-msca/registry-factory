"""Registry factory module for a codebase."""
from typing import Any, Dict, List, Optional, Type

from registry_factory.patterns.facade import ObserverFacade
from registry_factory.patterns.mediator import HashMediator
from registry_factory.patterns.observer import RegistryObserver
from registry_factory.registry import AbstractRegistry
from registry_factory.tracker import Tracker
from registry_factory.index import RegistryTable, HashTable


class Factory:
    """A factory class for creating registries."""

    _hash_map: RegistryTable
    _shared_hash: int
    _shared_hash_table: HashTable

    def __init__(self):
        raise ValueError("Factory is not meant to be instantiated.")

    @classmethod
    def hash_map(cls) -> RegistryTable:
        """Return the hash map."""
        if not hasattr(cls, "_hash_map"):
            cls.init_hash_map()
        return cls._hash_map

    @classmethod
    def shared_hash(cls) -> int:
        """Return the shared hash."""
        if not hasattr(cls, "_shared_hash"):
            cls.init_hash_map()
        return cls._shared_hash

    @classmethod
    def shared_hash_table(cls) -> HashTable:
        """Return the shared hash table."""
        if not hasattr(cls, "_shared_hash_table"):
            cls._shared_hash_table = HashTable()
        return cls._shared_hash_table

    @classmethod
    def init_hash_map(cls, bitsize=256, max_generation=1000) -> None:
        """Initialize the hash map."""
        cls._hash_map = RegistryTable(bitsize, max_generation)
        cls._shared_hash = cls._hash_map.generate_hash()

    @classmethod
    def create_registry(
        cls,
        shared: bool = False,
        skip_validation: bool = False,
        checks: Optional[List[RegistryObserver]] = None,
    ) -> Type[AbstractRegistry]:
        registry_hash = cls.shared_hash() if shared else cls.hash_map().generate_hash()

        class Registry(AbstractRegistry):
            _registry_hash = registry_hash
            mediator = HashMediator(registry_hash, ObserverFacade(skip_validation, observers=checks))

        if not shared:
            cls.hash_map().set(registry_hash)
        else:
            Registry.mediator.hash_table = cls.shared_hash_table()
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
