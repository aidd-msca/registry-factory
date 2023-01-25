from typing import Any
import warnings

from abstract_codebase.patterns.observer import RegistryObserver


class FactoryPattern(RegistryObserver):
    def __init__(self, factory_pattern: Any, forced: bool = False):
        super().__init__()
        self.forced = forced
        self.factory_pattern = factory_pattern

    def register_event(self, key: str, object: Any, **kwargs):
        if not issubclass(object, self.factory_pattern):
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

    def info(self, key: str) -> str:
        if self.index[key] is True:
            return f"{key} has the valid factory patten."
        else:
            return f"{key} has not the valid factory patten."
