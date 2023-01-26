from typing import Any
from types import FunctionType

import warnings

from registry_factory.patterns.observer import RegistryObserver


class FactoryPattern(RegistryObserver):
    """A factory pattern observer."""

    def __init__(self, factory_pattern: Any, forced: bool = False):
        super().__init__()
        self.forced = forced
        self.factory_pattern = factory_pattern
        if isinstance(self.factory_pattern, FunctionType):
            self.class_pattern = False
        else:
            self.class_pattern = True

    def register_event(self, key: str, object: Any, **kwargs):
        if not self._match_pattern(object):
            if self.forced:
                raise TypeError("Object must be a subclass of the factory pattern.")
            else:
                warnings.warn("Object must be a subclass of the factory pattern.")
                self.index[key] = False
        else:
            self.index[key] = True

    def call_event(self, key: str, **kwargs):
        pass

    def get_info(self, key: str) -> Any:
        return self.index[key]

    def _match_pattern(self, object: Any) -> bool:
        # function pattern
        if isinstance(object, FunctionType) and self.class_pattern is False:
            return object.__annotations__ == self.factory_pattern.__annotations__

        # class pattern
        if isinstance(type(object), self.factory_pattern) or type(object) == type:
            if issubclass(self.factory_pattern, object):
                return True
            elif issubclass(object, self.factory_pattern):
                return True
            elif all(
                hasattr(object, func)
                for func in [func for func in dir(self.factory_pattern) if not func.startswith("__")]
            ):
                return True
            else:
                return False

        return False

    def info(self, key: str) -> str:
        if self.index[key] is True:
            return f"{key} has the valid factory patten."
        else:
            return f"{key} has not the valid factory patten."
