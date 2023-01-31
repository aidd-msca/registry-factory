"""Mediator pattern implementation."""
from typing import Any, Dict, Optional, Tuple
from registry_factory.index import HashTable
from registry_factory.patterns.facade import ObserverFacade


class HashMediator:
    connection_hash: int
    hash_table: HashTable
    observer_facade: ObserverFacade

    def __init__(
        self, connection_hash: int, observer_facade: ObserverFacade, bitsize=256, max_generation=1000
    ) -> None:
        self.connection_hash = connection_hash
        self.observer_facade = observer_facade
        self.hash_table = HashTable(bitsize, max_generation)

    def generate_key_dict(self, key: str, **kwargs) -> Dict:
        return self.observer_facade.generate_key_dict(key=key, **kwargs)

    def register_event(self, key: str, obj: Any, **kwargs) -> None:
        key_dict = self.generate_key_dict(key=key, **kwargs)
        (key, key_dict, obj, meta_dict) = self.observer_facade.register_event(key=key, obj=obj, **kwargs)
        self.hash_table.set(key, key_dict, obj, meta_dict)

    def call_event(self, key: str, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
        key_dict = self.generate_key_dict(key=key, **kwargs)
        obj = self.hash_table.get(key, key_dict)
        (key, key_dict, obj, meta_dict) = self.observer_facade.call_event(key=key, obj=obj, **kwargs)
        return (key, key_dict, obj, meta_dict)

    def get_meta(self, key: str, **kwargs) -> Dict:
        key_dict = self.generate_key_dict(key=key, **kwargs)
        print("heya")
        print(key_dict)
        return self.hash_table.get_meta(key, key_dict)


class HashConnection:
    connection: Dict[int, HashMediator]

    def add_connection(self, connection_hash: int, mediator: HashMediator) -> None:
        self.connection[connection_hash] = mediator

    def get_connection(self, connection_hash: int) -> HashMediator:
        return self.connection[connection_hash]
