from typing import Any, Callable
import warnings
from registry_factory.patterns.observer import RegistryObserver


class Testing(RegistryObserver):
    """A testing observer."""

    def __init__(self, test_module: Callable, forced: bool = False):
        super().__init__()
        self.forced = forced
        self.test_module = test_module

    def register_event(self, key: str, object: Any, **kwargs):
        try:
            self.test_module(object)
            self.index[key] = True
        except Exception:
            if self.forced:
                raise AssertionError("Object must pass the test module.")
            else:
                warnings.warn("Object must pass the test module.")
                self.index[key] = False

    def call_event(self, key: str, **kwargs):
        pass

    def get_info(self, key: str) -> Any:
        return self.index[key]

    def info(self, key: str) -> str:
        if self.index[key] is True:
            return f"{key} has passed testing."
        else:
            return f"{key} has not passed testing."
