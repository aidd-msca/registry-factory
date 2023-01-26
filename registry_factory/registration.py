"""Registry module for a codebase."""
from abc import ABC
import warnings
from typing import Any, Callable, List, Optional, Dict

from registry_factory.patterns.facade import ObserverFacade
from registry_factory.index import IndexDict
from registry_factory.tracker import Tracker
from registry_factory.typescripts import Dataclass

__all__ = ["RegistrationError", "RegistrationWarning", "AbstractRegistry"]


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

    index: IndexDict
    arguments: IndexDict

    facade: ObserverFacade

    @classmethod
    def __call__(cls, key: str) -> None:
        """Return the object registered to the key."""
        raise NotImplementedError("Use the get method to call the registry.")

    @classmethod
    def __getitem__(cls, key: str) -> None:
        """Return the object registered to the key."""
        raise NotImplementedError("Use the get method to call the registry.")

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
            Tracker().add(key, cls.__name__)
            return cls.index.get(key)  # , **kwargs)
        else:
            cls.check_choice(key, **kwargs)
            Tracker().add(key, cls.__name__)
            return cls.index.get(key, default)  # , **kwargs)

    @classmethod
    def get_info(cls, key: str) -> Dict:
        """Return the meta information for the key."""
        return cls.facade.get_info(key)

    @classmethod
    def print_info(cls, key: str) -> None:
        """Return the meta information for the key."""
        cls.facade.print_info(key)

    @classmethod
    def register(cls, key: str, **kwargs) -> Callable:
        """Register the object to the key with the option to use as a decorator."""

        def wrapper(obj: Callable) -> Callable:
            """Register the object to the key."""
            if cls.facade is not None:
                cls.facade.register_event(key, obj, **kwargs)
            cls.index[key] = obj
            return obj

        return wrapper

    @classmethod
    def register_prebuilt(cls, obj: object, key: str, **kwargs):
        """Register the object to the key."""
        cls.register(key, **kwargs)(obj)

    @classmethod
    def show_choices(cls) -> List[str]:
        """Returns the indexes of all registered objects."""
        return list(cls.index.keys())

    @classmethod
    def check_choice(cls, key: str, **kwargs) -> bool:
        """Checks if a choice is valid and returns a bool."""
        if key not in cls.index.keys():
            warnings.warn(RegistrationWarning(f"{key} is not a valid choice."))
            return False
        elif cls.facade is not None:
            cls.facade.call_event(key, **kwargs)
        return True

    @classmethod
    def validate_choice(cls, key: str, **kwargs) -> str:
        """Checks if a choice is valid and stops if not."""
        if key not in cls.index.keys():
            raise RegistrationError(f"{key} is not a valid choice.")
        elif cls.facade is not None:
            cls.facade.call_event(key, **kwargs)
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
