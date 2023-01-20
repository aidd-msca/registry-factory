"""Postchecks for a registry."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

from abstract_codebase.accreditation import Accreditation


__all__ = ["CreditType", "CreditInfo"]


class AbstractPostCheck(ABC):
    @abstractmethod
    def validate_call(self, key: str, **kwargs) -> None:
        """Validate the call."""
        raise NotImplementedError

    @abstractmethod
    def validate_register(self, object: Any, key: str, **kwargs) -> None:
        """Validate a new function registered."""
        raise NotImplementedError


class AccreditationPostCheck(AbstractPostCheck):
    """Postchecks for accreditation."""

    # accreditation: Accreditation = Accreditation()

    def __init__(self, forced: bool = False) -> None:
        self.forced = forced
        self.accreditation = Accreditation()

    def validate_call(self, key: str, **kwargs) -> None:
        """Validate the call."""
        self.accreditation.called(key)

    def validate_register(self, object: Any, key: str, **kwargs) -> None:
        """Validate a new function registered."""
        print(kwargs)
        print("credit" in kwargs.keys())
        print("credit_type" in kwargs.keys())

        if "credit" in kwargs.keys() and "credit_type" in kwargs.keys():
            self.accreditation.add_credit(key, kwargs["credit"], kwargs["credit_type"])
        else:
            if self.forced:
                raise ValueError("Credit and credit type must be specified.")


class CreditType(Enum):
    """Credit options:
    Reference requires reference to a paper/publication.
    Acknowledgement requires a mention in the acknowledgements.
    None requires no credit.
    Other is a placeholder for additional undefined or collaboration-specific credit types.
    """

    REFERENCE = auto()
    ACKNOWLEDGEMENT = auto()
    NONE = auto()
    OTHER = auto()


@dataclass
class CreditInfo:
    """Credit information."""

    author: str
    github: Optional[str] = None
    url: Optional[str] = None
    additional_information: Optional[str] = None

    def __str__(self) -> str:
        """Return the string representation."""
        authors = f"author -{self.author} ({self.github})" if self.github else f"{self.author}"
        url = f"\n url - {self.url}" if self.url is None else ""
        additional_information = (
            f"\n additional info - {self.additional_information}" if self.additional_information is None else ""
        )
        return f"{authors}{url}{additional_information}"
