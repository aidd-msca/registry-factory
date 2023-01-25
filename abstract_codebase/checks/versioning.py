from typing import Any
from abstract_codebase.patterns.observer import MetaInformationObserver
from dataclasses import dataclass


@dataclass
class VersioningFields:
    version: str
    date: str


class Versioning(MetaInformationObserver):
    def __init__(self, version_fields: Any = VersioningFields, forced: bool = False):
        super().__init__(meta_fields=version_fields, forced=forced)
