from abc import ABC, abstractmethod
import inspect
from typing import Any, Dict
import warnings
from registry_factory.patterns.metacoding import UniqueDict
from dataclasses import fields, is_dataclass, asdict


class RegistryObserver(ABC):
    index: Dict[str, Any] = UniqueDict()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def register_event(self, key: str, object: Any, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def call_event(self, key: str, **kwargs):
        raise NotImplementedError

    def get_info(self, key: str) -> Any:
        return self.index[key]

    def info(self, key: str) -> str:
        pass


class MetaInformationObserver(RegistryObserver):
    def __init__(self, meta_fields: Any, forced: bool = False):
        self.forced = forced
        if not is_dataclass(meta_fields):
            raise TypeError("Fields must be a dataclass.")
        self.meta_fields = meta_fields
        self.parameters = [p for p in inspect.signature(self.meta_fields).parameters]

    def register_event(self, key: str, object: Any, **kwargs):
        missing_fields = []
        for p in self.parameters:
            if p not in kwargs.keys():
                missing_fields.append(p)
        if missing_fields != [] and self.forced:
            raise ValueError(f"Information must have a {', '.join(missing_fields)} field.")
        elif missing_fields == []:
            test = self.meta_fields(
                **{k: v for k, v in kwargs.items() if k in inspect.signature(self.meta_fields).parameters}
            )
            self.index[key] = test
        else:
            warnings.warn(f"Information must have a {', '.join(missing_fields)} field.")

    def call_event(self, key: str, **kwargs):
        try:
            for field in fields(self.index[key]):
                assert kwargs[field.name] == getattr(self.index[key], field.name)
        except Exception as e:
            if self.forced:
                raise e
            else:
                warnings.warn(str(e))

    def get_info(self, key: str) -> Any:
        return asdict(self.index[key])

    def info(self, key: str) -> str:
        name_values = {
            ", ".join([f"{field.name}: {getattr(self.index[key], field.name)}" for field in fields(self.index[key])])
        }
        return f"{name_values}"
