"""Accreditation postchecks for a codebase."""

from typing import Any, List, Optional
from registry_factory.patterns.observer import MetaInformationObserver
from dataclasses import dataclass

__all__ = ["Accreditation", "CreditFields"]


@dataclass
class CreditFields:
    """Credit information."""

    author: str
    credit_type: str
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


class Accreditation(MetaInformationObserver):
    def __init__(self, credit_fields: Any = CreditFields, key_list: List = [], forced: bool = False):
        super().__init__(meta_fields=credit_fields, key_parameters=key_list, forced=forced)
