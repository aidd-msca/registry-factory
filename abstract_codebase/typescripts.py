"""Script to define codebase-wide typescripts."""

from typing import Dict, Protocol

__all__ = ["Dataclass"]


class Dataclass(Protocol):
    __dataclass_fields__: Dict
