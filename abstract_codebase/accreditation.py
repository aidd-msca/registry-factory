"""Accreditations for a Codebase."""

from typing import Dict, Optional, Set, Tuple

from abstract_codebase.metacoding import Singleton, UniqueDict

__all__ = ["Accreditation"]


class Accreditation(Singleton):
    """Class to manage accreditations and keeping track of called objects."""

    accreditations: Dict[str, Tuple[Dict, str]] = UniqueDict()
    called_objects: Set[str] = set()

    def add_credit(
        self,
        index: str,
        credit: Dict,
        credit_type: Optional[str] = None,
    ):
        """Add an accreditation."""
        self.accreditations[index] = (credit, credit_type if credit_type is not None else "no credit")

    def get(self, index: str) -> Tuple[Dict, str]:
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
