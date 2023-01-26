"""Accreditation postchecks for a codebase."""

from typing import Any, Optional
from registry_factory.patterns.observer import MetaInformationObserver
from dataclasses import dataclass, fields

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
    def __init__(self, version_fields: Any = CreditFields, forced: bool = False):
        super().__init__(meta_fields=version_fields, forced=forced)

    def get(self, key: str) -> Any:
        """Return the object."""
        name_values = {", ".join([f"{field.name}: {getattr(self, field.name)}" for field in fields(self.index[key])])}
        return f"Credit({name_values})"
