"""Facade dealing with calling and registering postchecks for a registry."""

from typing import Any, Dict, List, Optional
from registry_factory.patterns.observer import RegistryObserver

__all__ = ["ObserverFacade"]


class ObserverFacade:
    """Facade dealing with calling and registering postchecks for a registry."""

    _observers: Optional[Dict[str, RegistryObserver]]

    def __init__(self, observers: Optional[List[RegistryObserver]]) -> None:
        if observers is None or len(observers) == 0:
            self._observers = None
        else:
            self._observers = {obj.name: obj for obj in observers}

    def compose_register(self, key: str, object: Any, skip_val: bool = False, **kwargs: Any) -> None:
        if self._observers is None:
            return
        errors = []
        for idx in self._observers.values():
            try:
                idx.register_event(object, key, **kwargs)
            except Exception as e:
                errors.append(f"{idx.name}:\t{e}")
        if len(errors) > 0 and skip_val is False:
            raise Exception("\n".join(errors))

    def compose_call(self, key: str, skip_val: bool, **kwargs) -> None:
        if self._observers is None:
            return
        errors = []
        for idx in self._observers.values():
            try:
                idx.call_event(key, **kwargs)
            except Exception as e:
                errors.append(f"{idx.name}:\t{e}")
        if len(errors) > 0 and skip_val is False:
            raise Exception("\n".join(errors))

    def register_event(self, key: str, object: Any, skip_val: bool = False, **kwargs) -> None:
        self.compose_register(object, key, skip_val=skip_val, **kwargs)

    def call_event(self, key: str, skip_val: bool = False, **kwargs) -> Any:
        if self._observers is not None:
            self.compose_call(key, skip_val=skip_val, **kwargs)

    def get_info(self, key: str) -> Dict:
        if self._observers is None:
            return {}
        return {idx.name: idx.get_info(key) for idx in self._observers.values()}

    def show_registered(self) -> None:
        if self._observers is None:
            return
        for idx in self._observers.values():
            print(idx.index)

    def print_info(self, key: str) -> None:
        if self._observers is not None:
            for idx in self._observers.values():
                print(f"{idx.name}: ({idx.info(key)})")
