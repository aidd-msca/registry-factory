from typing import Optional
import warnings
from registry_factory.patterns.metacoding import UniqueDict


class IndexDict(UniqueDict):
    """Dict that raises when reassigning an existing key."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if "shared" in kwargs:
            if kwargs["shared"] is True:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                elif "warnings" in kwargs:
                    if kwargs["warnings"] is True:
                        warnings.warn("SharedIndexDict already exists, overriding with new instance.")
                return cls._instance

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, shared: Optional[bool] = None, warnings: Optional[bool] = None) -> None:
        super().__init__()
