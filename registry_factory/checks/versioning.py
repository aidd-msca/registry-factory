from typing import Any, List
from registry_factory.patterns.observer import MetaInformationObserver
from dataclasses import dataclass


@dataclass
class VersioningFields:
    version: str
    date: str


class Versioning(MetaInformationObserver):
    def __init__(self, version_fields: Any = VersioningFields, key_list: List = ["version"], forced: bool = False):
        super().__init__(meta_fields=version_fields, key_parameters=key_list, forced=forced)
