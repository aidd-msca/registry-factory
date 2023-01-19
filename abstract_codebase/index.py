"""Index variants for registries."""


# TODO
# Add test cases for reset method

# add sharing using @property
# add accreditation with custom credit type
# add forced accreditation
# add versioning
# add versioning with custom version type
# add forced versioning
# add factory pattern
# add factory pattern with custom factory type
# add forced factory pattern
# add forced arguments

# add automatic init arguments
# import inspect
# >>> inspect.signature(Super.__init__)

# Factory pattern type hint


# raise warning when there are unused kwargs

from typing import List, Optional, Type

from abstract_codebase.postchecks import AbstractPostCheck


class IndexDict(dict):
    """Dict that raises when reassigning an existing key."""

    def __init__(self, post_checks: Optional[List[Type[AbstractPostCheck]]] = None) -> None:
        super().__init__()
        self.post_checks = post_checks

    def __setitem__(self, key, value, **kwargs):
        if self.__contains__(key):
            raise KeyError("Key already in dict.")
        else:
            if self.post_checks is not None:
                self.register_postcheck(self, value, key, **kwargs)
            super().__setitem__(key, value)

    def __getitem__(self, key, **kwargs):
        if self.__contains__(key):
            if self.post_checks is not None:
                self.call_postcheck(self, key, **kwargs)
            return super().__getitem__(key)
        else:
            raise KeyError("Key not in dict.")

    def call_postcheck(self, key, **kwargs) -> None:
        if self.post_checks is not None:
            for postcheck in self.post_checks:
                postcheck.validate_call(key, **kwargs)

    def register_postcheck(self, object, key, **kwargs) -> None:
        if self.post_checks is not None:
            for postcheck in self.post_checks:
                postcheck.validate_register(object, key, **kwargs)


class SharedIndexDict(IndexDict):
    """Dict that raises when reassigning an existing key.
    Only allows one instance to exist, new instances get overridden."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
