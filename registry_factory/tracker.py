"""Call tracker."""

from typing import Dict, Set
from registry_factory.patterns.metacoding import Singleton

__all__ = ["Tracker"]


class Tracker(Singleton):
    called: Set = set()
    called_meta: Dict = dict()

    def add(self, key: str, registry: str) -> None:
        self.called.add(f"{key} ({registry})")

    def add_meta(self, key: str, registry: str, information_string: str) -> None:
        self.called_meta[f"{key} ({registry})"] = information_string

    def get(self) -> Set:
        return self.called

    def show(self) -> None:
        for key in self.called:
            print(f"{key}: {self.called_meta[key]}")
