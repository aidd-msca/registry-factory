"""Facade dealing with calling and registering postchecks for a registry."""

from typing import Any, Dict, List, Optional, Tuple
from registry_factory.patterns.observer import RegistryObserver

__all__ = ["ObserverFacade"]


class ObserverFacade:
    observers: Optional[List[RegistryObserver]]

    def __init__(self, skip_val: bool = False, observers: Optional[List[RegistryObserver]] = None) -> None:
        self.skip_val = skip_val

        if observers is None or len(observers) == 0:
            self.observers = None
        else:
            self.observers = observers

    def generate_key_dict(self, key: str, **kwargs) -> Dict:
        if self.observers is None:
            return {}
        key_dict: Dict = {}
        for observer in self.observers:
            obs_key_dict = observer.generate_key_dict(key=key, **kwargs)
            key_dict = {**key_dict, **obs_key_dict}

        return key_dict

    def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        if self.observers is None:
            return (key, {}, obj, None)
        errors = []
        key_dict: Dict = {}
        meta_dict: Dict = {}
        for observer in self.observers:
            try:
                _, obs_key_dict, _, obs_meta_dict = observer.register_event(key=key, obj=obj, **kwargs)
                key_dict = {**key_dict, **obs_key_dict}
                meta_dict = {**meta_dict, **obs_meta_dict} if obs_meta_dict is not None else meta_dict
            except Exception as e:
                errors.append(f"{e}")
        if len(errors) > 0 and self.skip_val is False:
            raise Exception("\n".join(errors))
        return (key, key_dict, obj, meta_dict)

    def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        if self.observers is None:
            return (key, {}, obj, None)
        errors = []
        key_dict: Dict = {}
        meta_dict: Dict = {}
        for observer in self.observers:
            try:
                _, obs_key_dict, _, obs_meta_dict = observer.call_event(key=key, obj=obj, **kwargs)
                key_dict = {**key_dict, **obs_key_dict}
                meta_dict = {**meta_dict, **obs_meta_dict} if obs_meta_dict is not None else meta_dict
            except Exception as e:
                errors.append(f"{e}")
        if len(errors) > 0 and self.skip_val is False:
            raise Exception("\n".join(errors))
        return (key, key_dict, obj, meta_dict)
