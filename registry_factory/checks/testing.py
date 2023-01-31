from typing import Any, Callable, Dict, Optional, Tuple
import warnings
from registry_factory.patterns.observer import RegistryObserver


class Testing(RegistryObserver):
    """A testing observer."""

    def __init__(self, test_module: Callable, forced: bool = False):
        super().__init__()
        self.forced = forced
        self.test_module = test_module

    def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        try:
            self.test_module(key, obj, **kwargs)
            passed_test = True
        except Exception:
            if self.forced:
                raise AssertionError("Object must pass the test module.")
            else:
                warnings.warn("Object must pass the test module.")
                passed_test = False
        return (key, {}, obj, {"passed_test": passed_test})

    def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        return (key, {}, obj, None)
