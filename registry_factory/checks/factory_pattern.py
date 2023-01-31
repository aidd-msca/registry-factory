from typing import Any, Dict, Optional, Tuple
from types import FunctionType

import warnings

from registry_factory.patterns.observer import RegistryObserver


class FactoryPattern(RegistryObserver):
    """An instance factory pattern observer."""

    def __init__(self, factory_pattern: Any, forced: bool = False):
        super().__init__()
        self.forced = forced
        self.factory_pattern = factory_pattern
        if isinstance(self.factory_pattern, FunctionType):
            self.class_pattern = False
        else:
            self.class_pattern = True

    def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        if not self._match_pattern(obj):
            if self.forced:
                raise TypeError("Object must be a subclass of the factory pattern.")
            else:
                warnings.warn("Object must be a subclass of the factory pattern.")
                passed_test = False
        else:
            passed_test = True
        return (key, {}, obj, {"correct_pattern": passed_test})

    def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        return (key, {}, obj, None)

    def _match_pattern(self, obj: Any) -> bool:
        # function pattern
        if isinstance(obj, FunctionType) and self.class_pattern is False:
            return obj.__annotations__ == self.factory_pattern.__annotations__

        # class pattern
        if isinstance(type(obj), self.factory_pattern) or type(obj) == type:
            if issubclass(self.factory_pattern, obj):
                return True
            elif issubclass(obj, self.factory_pattern):
                return True
            elif all(
                hasattr(obj, func)
                for func in [func for func in dir(self.factory_pattern) if not func.startswith("__")]
            ):
                return True
            else:
                return False

        return False
