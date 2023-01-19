"""Postchecks for a registry."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional


__all__ = ["CreditType", "CreditInfo"]


class AbstractPostCheck(ABC):
    @abstractmethod
    def validate_call(self, key, **kwargs) -> bool:
        """Validate the call."""
        raise NotImplementedError

    @abstractmethod
    def validate_register(self, object, key, **kwargs) -> bool:
        """Validate a new function registered."""
        raise NotImplementedError


# cls.checks.called(key)

# if credit is not None:
#     cls.accreditation.add_credit(key, credit, credit_type)


class partial(dict):
    @classmethod
    def credit_postcheck(cls, credit: Dict) -> Any:
        return CreditInfo(credit)

    @classmethod
    def credit_type_postcheck(cls) -> Any:
        return CreditType

    @classmethod
    def version_postcheck(cls) -> Any:
        return str


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
