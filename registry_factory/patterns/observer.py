from abc import ABC, abstractmethod
import inspect
from typing import Any, Dict, List, Optional, Tuple
import warnings
from dataclasses import is_dataclass


class RegistryObserver(ABC):
    def generate_key_dict(self, key: str, **kwargs) -> Dict:
        return {}

    @abstractmethod
    def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        raise NotImplementedError

    @abstractmethod
    def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        raise NotImplementedError


class MetaInformationObserver(RegistryObserver):
    def __init__(self, meta_fields: Any, key_parameters: List[str], forced: bool = False):
        self.forced = forced
        if not is_dataclass(meta_fields):
            raise TypeError("Fields must be a dataclass.")
        self.key_parameters = key_parameters
        self.meta_fields = meta_fields
        self.parameters = [p for p in inspect.signature(self.meta_fields).parameters]

    def generate_key_dict(self, key: str, **kwargs) -> Dict:
        return {k: v for k, v in kwargs.items() if k in self.key_parameters}

    def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        register_dict = {}
        missing_fields = []
        for p in self.parameters:
            if p not in kwargs.keys():
                missing_fields.append(p)
            else:
                register_dict[p] = kwargs[p]

        key_dict = self.generate_key_dict(key=key, **kwargs)
        meta_dict = {k: v for k, v in register_dict.items() if k not in key_dict}

        if missing_fields != [] and self.forced:
            raise ValueError(f"Information must have a {', '.join(missing_fields)} field.")
        elif missing_fields != [] and not self.forced:
            warnings.warn(f"Information should have a {', '.join(missing_fields)} field.")
        return (key, key_dict, obj, meta_dict)

    def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        call_dict = {}
        missing_fields = []
        for p in self.parameters:
            if p not in kwargs.keys():
                missing_fields.append(p)
            else:
                call_dict[p] = kwargs[p]

        key_dict = self.generate_key_dict(key=key, **kwargs)
        meta_dict = {k: v for k, v in call_dict.items() if k not in key_dict}

        if missing_fields != [] and self.forced:
            raise ValueError(f"Information must have a {', '.join(missing_fields)} field.")
        elif missing_fields != [] and not self.forced:
            warnings.warn(f"Information should have a {', '.join(missing_fields)} field.")
        return (key, key_dict, obj, meta_dict)
