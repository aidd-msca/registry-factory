"""Call tracker."""

from typing import Dict, Optional, Set
from registry_factory.patterns.metacoding import Singleton

__all__ = ["Tracker"]


class Tracker(Singleton):
    called: Set[Dict] = set()

    def add(self, registry: int, key: str, key_dict: Optional[Dict]) -> None:
        self.called.add({registry: (key, key_dict)})

    def get(self) -> Set:
        return self.called

    def show(self) -> None:
        for registry, full_key in self.called:
            print(f"{registry}: {full_key}")
