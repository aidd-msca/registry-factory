"""Accreditations for a Codebase."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, Optional, Set, Tuple

from abstract_codebase.metacoding import Singleton, UniqueDict

__all__ = ["CreditType", "CreditInfo", "Accreditation"]


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


class Accreditation(Singleton):
    """Class to manage accreditations and keeping track of called objects."""

    accreditations: Dict[str, Tuple[CreditInfo, CreditType]] = UniqueDict()
    called_objects: Set[str] = set()

    def add_credit(
        self, index: str, credit: CreditInfo, credit_type: CreditType = CreditType.NONE,
    ):
        """Add an accreditation."""
        self.accreditations[index] = (credit, credit_type)

    def get(self, index: str) -> Tuple[CreditInfo, CreditType]:
        """Returns the accreditation information for a given index."""
        return self.accreditations[index]

    def register_accreditation(self, index: str) -> None:
        """Registers an called objects."""
        if index in self.accreditations.keys():
            self.called_objects.add(index)

    def called(self, index: str) -> None:
        """Registers a called objects."""
        self.register_accreditation(index)

    def show_accreditations(self) -> None:
        """Prints the accreditations."""
        for called in self.called_objects:
            print(called, self.accreditations.get(called))

    def show_all_accreditations(self) -> None:
        """Prints the accreditations."""
        for called in self.accreditations.keys():
            print(called, self.accreditations.get(called))
