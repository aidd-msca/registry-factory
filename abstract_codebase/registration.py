"""Registration factory module for a codebase."""
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple

from abstract_codebase.accreditation import Accreditation, CreditInfo, CreditType
from abstract_codebase.metacoding import UniqueDict
from abstract_codebase.typescripts import Dataclass


# TODO
# Add reset method to RegistryFactory
# Add test cases for reset method
# add sharing using @property
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


class RegistryFactory:
    """Factory to generate a registry."""

    index: Dict[str, object] = UniqueDict()
    arguments: Dict[str, Dataclass] = UniqueDict()

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
    def get(cls, key: str, default: Optional[object] = None) -> object:
        """Return the object registered to the key."""
        cls.accreditation.called(key)
        cls.validate_choice(key)
        return cls.index.get(key, default)

    @classmethod
    def register(
        cls,
        key: str,
        credit: Optional[CreditInfo] = None,
        credit_type: CreditType = CreditType.NONE,
    ) -> Callable:
        """Register the object to the key with the option to use as a decorator."""
        # if key in cls.index:
        #     warnings.warn(RegistrationWarning(f"{key} is already registered to {cls.index[key]}."))

        def wrapper(obj: object) -> object:
            """Register the object to the key."""
            cls.index[key] = obj
            if credit is not None:
                cls.accreditation.add_credit(key, credit, credit_type)
            return obj

        return wrapper

    @classmethod
    def register_prebuilt(
        cls,
        obj: object,
        key: str,
        credit: Optional[CreditInfo] = None,
        credit_type: CreditType = CreditType.NONE,
    ):
        """Register the object to the key."""
        cls.register(key, credit, credit_type)(obj)

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

    @classmethod
    def get_info(cls, key: str) -> Tuple[CreditInfo, CreditType]:
        """Return the accreditation information for the key."""
        return cls.accreditation.get(key)

    @classmethod
    def get_choice(cls, key: str) -> object:  # Legacy
        """Legacy: Returns an object from the index."""
        return cls.get(key)

    @classmethod
    def show_choices(cls) -> List[str]:
        """Returns the indexes of all registered objects."""
        return List(cls.index.keys())

    @classmethod
    def view_accreditations(cls) -> None:
        """View the accreditation information."""
        print("accreditations:")
        cls.accreditation.show_accreditations()

    @classmethod
    def check_choice(cls, key: str) -> bool:
        """Checks if a choice is valid and returns a bool."""
        if key not in cls.index.keys():
            warnings.warn(RegistrationWarning(f"{key} is not a valid choice."))
            return False
        return True

    @classmethod
    def validate_choice(cls, key: str) -> None:
        """Checks if a choice is valid and stops if not."""
        if key not in cls.index.keys():
            raise RegistrationError(f"{key} is not a valid choice.")

    @classmethod
    def get_subclass_arguments(cls, argument_classes: Dict[str, Dict]) -> Dict[str, Any]:
        """Return the arguments for the subclass."""
        dataclasses = {}

        RegistryClasses = cls.__subclasses__()
        registries = {reg.__name__.lower(): reg for reg in RegistryClasses}
        for name, selection in argument_classes.items():
            for (registry, call) in selection.items():
                dataclasses[name] = registries[registry].get_arguments(call)

        return dataclasses

    @classmethod
    def get_subclass_choices(cls, choices: Dict[str, Dict]) -> Dict[str, Any]:
        """Return the choices for the subclass."""
        objects = {}

        RegistryClasses = cls.__subclasses__()
        registries = {reg.__name__.lower(): reg for reg in RegistryClasses}
        for name, selection in choices.items():
            for (registry, call) in selection.items():
                objects[name] = registries[registry].get_choice(call)

        return objects
