"""Registry module for a codebase."""
from abc import ABC
import warnings
from typing import Any, Callable, List, Optional, Dict, Tuple

# from registry_factory.tracker import Tracker
from registry_factory.patterns.mediator import HashMediator
from registry_factory.typescripts import Dataclass
from registry_factory.utils import RegistrationError, RegistrationWarning

__all__ = ["AbstractRegistry"]


class AbstractRegistry(ABC):
    """Abstract class to generate a registry."""

    _registry_hash: int
    mediator: HashMediator

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @classmethod
    def __call__(cls, key: str) -> None:
        """Return the object registered to the key."""
        raise NotImplementedError("Use the get() method to call the registry.")

    @classmethod
    def __getitem__(cls, key: str) -> None:
        """Return the object registered to the key."""
        raise NotImplementedError("Use the get() method to call the registry.")

    @classmethod
    def __contains__(cls, key: str, **kwargs) -> bool:
        """Return True if the key is registered."""
        key_dict = cls.mediator.generate_key_dict(key=key, **kwargs)
        return (key, key_dict) in cls.mediator.hash_table.slots.values()

    @classmethod
    def __len__(cls) -> int:
        """Return the number of registered keys."""
        return len(cls.mediator.hash_table.slots)

    @classmethod
    def __iter__(cls) -> List[Tuple[str, Dict]]:
        """Return a list of registered keys."""
        return list(cls.mediator.hash_table.slots.values())

    @classmethod
    def __str__(cls) -> str:
        """Return a string representation of the registry."""
        return f"{cls.__name__}({cls.mediator.hash_table.slots})"

    @classmethod
    def __repr__(cls) -> str:
        """Return a string representation of the registry."""
        return f"{cls.__name__}({cls.mediator.hash_table.slots})"

    @classmethod
    def register(cls, key: str, **kwargs) -> Callable:
        """Register the object to the key with the option to use as a decorator."""

        def wrapper(obj: Callable) -> Callable:
            """Register the object to the key."""
            cls.mediator.register_event(key=key, obj=obj, **kwargs)
            return obj

        return wrapper

    @classmethod
    def register_prebuilt(cls, obj: object, key: str, **kwargs):
        """Register the object to the key."""
        cls.register(key, **kwargs)(obj)

    @classmethod
    def get(cls, key: str, default: Optional[Any] = None, **kwargs) -> Any:
        """Return the object registered to the key."""
        try:
            key, key_dict, obj, _ = cls.mediator.call_event(key=key, **kwargs)
            # Tracker().add(cls._registry_hash, key, key_dict)
        except Exception as e:
            if default is None:
                raise RegistrationError(f"{key} is not registered.") from e
            else:
                warnings.warn(f"{key} is not registered. Returning default.", RegistrationWarning)
                return default
        return obj

    @classmethod
    def get_info(cls, key: str, **kwargs) -> Dict:
        """Return the meta information for the key."""
        return cls.mediator.get_meta(key, **kwargs)

    @classmethod
    def show_choices(cls) -> List[Tuple[str, Dict]]:
        """Returns the indexes of all registered objects."""
        return list(cls.mediator.hash_table.slots.values())

    @classmethod
    def check_choice(cls, key: str, **kwargs) -> bool:
        """Checks if a choice is valid and returns a bool."""
        key_dict = cls.mediator.generate_key_dict(key=key, **kwargs)
        if (key, key_dict) not in cls.mediator.hash_table.slots.values():
            warnings.warn(RegistrationWarning(f"{key} is not a valid choice."))
            return False
        return True

    @classmethod
    def validate_choice(cls, key: str, **kwargs) -> None:
        """Checks if a choice is valid and stops if not."""
        key_dict = cls.mediator.generate_key_dict(key=key, **kwargs)
        if (key, key_dict) not in cls.mediator.hash_table.slots.values():
            raise RegistrationError(f"{key} is not a valid choice.")

    @classmethod
    def reset(cls):
        """Reset the registry."""
        cls.mediator.hash_table.clear()

    @classmethod
    def register_arguments(cls, key: str, **kwargs) -> Callable:
        """Register the arguments to the key."""

        def wrapper(argument_class: Dataclass) -> Any:
            key_dict = cls.mediator.generate_key_dict(key=key, **kwargs)
            cls.mediator.hash_table.set_arguments(key, key_dict, argument_class)
            return argument_class

        return wrapper

    @classmethod
    def get_arguments(cls, key: str, **kwargs) -> Dataclass:
        """Return the arguments registered to the key."""
        key_dict = cls.mediator.generate_key_dict(key=key, **kwargs)
        return cls.mediator.hash_table.get_arguments(key, key_dict)

    # Legacy methods
    @classmethod
    def get_choice(cls, key: str, **kwargs) -> Any:  # Legacy
        """Legacy: Returns an object from the index."""
        return cls.get(key, **kwargs)
