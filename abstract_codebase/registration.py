"""Registration factory module for a codebase."""
from abc import ABC
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Type

from abstract_codebase.accreditation import Accreditation
from abstract_codebase.index import IndexDict, SharedIndexDict
from abstract_codebase.postchecks import AbstractPostCheck
from abstract_codebase.typescripts import Dataclass


# TODO
# Add test cases for reset method
# add accreditation with custom credit type
# add forced accreditation
# add versioning
# add versioning with custom version type
# add forced versioning
# add factory pattern
# add factory pattern with custom factory type
# add forced factory pattern
# add forced arguments
# add automatic init arguments


class RegistrationError(Exception):
    """Registration error."""

    def __init__(self, message: str):
        """Initialize the RegistrationError."""
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the string representation of the RegistrationError."""
        return f"RegistrationError: {self.message}"


class RegistrationWarning(Warning):
    """Registration warning."""

    def __init__(self, message: str):
        """Initialize the RegistrationWarning."""
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the string representation of the RegistrationWarning."""
        return f"RegistrationWarning: {self.message}"


class AbstractRegistry(ABC):
    """Abstract class to generate a registry."""

    index: Dict[str, Callable]
    arguments: Dict[str, Dataclass]

    accreditation: Accreditation = Accreditation()

    @classmethod
    def __call__(cls, key: str) -> object:
        """Return the object registered to the key."""
        return cls.index[key]

    @classmethod
    def __getitem__(cls, key: str) -> object:
        """Return the object registered to the key."""
        return cls.index[key]

    @classmethod
    def __contains__(cls, key: str) -> bool:
        """Return True if the key is registered."""
        return key in cls.index

    @classmethod
    def __len__(cls) -> int:
        """Return the number of registered keys."""
        return len(cls.index)

    @classmethod
    def __iter__(cls) -> List[str]:
        """Return a list of registered keys."""
        return list(cls.index.keys())

    @classmethod
    def __str__(cls) -> str:
        """Return a string representation of the registry."""
        return f"{cls.__name__}({cls.index})"

    @classmethod
    def __repr__(cls) -> str:
        """Return a string representation of the registry."""
        return f"{cls.__name__}({cls.index})"

    @classmethod
    def get(cls, key: str, default: Optional[object] = None, **kwargs) -> object:
        """Return the object registered to the key."""
        if default is None:
            cls.validate_choice(key, **kwargs)
            return cls.index[key]
        else:
            cls.check_choice(key, **kwargs)
            return cls.index.get(key, default)

    @classmethod
    def register(cls, key: str, **kwargs) -> Callable:
        """Register the object to the key with the option to use as a decorator."""

        def wrapper(obj: Callable) -> Callable:
            """Register the object to the key."""
            cls.index[key] = obj  # **kwargs)
            return obj

        return wrapper

    @classmethod
    def register_prebuilt(cls, obj: object, key: str, **kwargs):
        """Register the object to the key."""
        cls.register(key, **kwargs)(obj)

    @classmethod
    def show_choices(cls) -> List[str]:
        """Returns the indexes of all registered objects."""
        return List(cls.index.keys())

    @classmethod
    def check_choice(cls, key: str, **kwargs) -> bool:
        """Checks if a choice is valid and returns a bool."""
        if key not in cls.index.keys():
            warnings.warn(RegistrationWarning(f"{key} is not a valid choice."))
            return False
        return True

    @classmethod
    def validate_choice(cls, key: str) -> str:
        """Checks if a choice is valid and stops if not."""
        if key not in cls.index.keys():
            raise RegistrationError(f"{key} is not a valid choice.")
        return key

    @classmethod
    def reset(cls):
        """Reset the registry."""
        cls.index.clear()

    @classmethod
    def register_arguments(cls, key: str) -> Callable:
        """Register the arguments to the key."""

        def wrapper(argument_class: Dataclass) -> Any:
            cls.arguments[key] = argument_class
            return argument_class

        return wrapper

    @classmethod
    def get_arguments(cls, key: str) -> Dataclass:
        """Return the arguments registered to the key."""
        return cls.arguments[key]

    # Legacy methods
    @classmethod
    def get_choice(cls, key: str) -> object:  # Legacy
        """Legacy: Returns an object from the index."""
        return cls.get(key)


class Factory:
    """A factory class for creating registries."""

    accreditation: Accreditation = Accreditation()

    @classmethod
    def create_registry(
        cls, shared: bool = False, post_checks: Optional[List[Type[AbstractPostCheck]]] = None
    ) -> Type[AbstractRegistry]:
        class Registry(AbstractRegistry):
            index = IndexDict(post_checks) if not shared else SharedIndexDict(post_checks)
            arguments = IndexDict(post_checks) if not shared else SharedIndexDict(post_checks)

        return Registry

    @classmethod
    def view_accreditations(cls) -> None:
        """View the accreditation information."""
        print("accreditations:")
        cls.accreditation.show_accreditations()

    @classmethod
    def get_info(cls, key: str) -> Tuple[Dict, str]:
        """Return the accreditation information for the key."""
        return cls.accreditation.get(key)

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
