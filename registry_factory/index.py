from typing import Any, Dict, Optional, Tuple
import warnings
from registry_factory.patterns.metacoding import Singleton, UniqueDict
import random


class IndexDict(UniqueDict):
    """Dict that raises when reassigning an existing key."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if "shared" in kwargs:
            if kwargs["shared"] is True:
                if cls._instance is None:
                    cls._instance = super().__new__(cls, *args, **kwargs)
                elif "warnings" in kwargs:
                    if kwargs["warnings"] is True:
                        warnings.warn("SharedIndexDict already exists, overriding with new instance.")
                return cls._instance

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, shared: Optional[bool] = None, warnings: Optional[bool] = None) -> None:
        super().__init__()


class HashTable(Singleton):
    """Hash table."""

    slots: Dict[int, Tuple[str, Dict]]
    data: Dict[int, Any]
    meta_dict: Dict[int, Dict]

    def __init__(self):
        self.bitsize = 256
        self.max_generation = 1000

    def generate_hash(self):
        key_hash = random.getrandbits(self.bitsize)

        current_generation = 0
        while key_hash in self.slots and current_generation < self.max_generation:
            key_hash = self.generate_hash()
            current_generation += 1

        return key_hash

    def set(self, key: str, key_dict: Dict, value: Any, meta: Optional[Dict] = None) -> None:
        full_key: Tuple[str, Dict] = (key, key_dict)
        if full_key in self.slots.values():
            raise KeyError(f"{key}, {key_dict} already exist in the registry.")

        hash_value = self.generate_hash()
        self.slots[hash_value] = full_key
        self.data[hash_value] = value
        if meta is not None:
            self.meta_dict[hash_value] = meta

    def set_meta(self, key: str, key_dict: Dict, meta: Dict) -> None:
        hash_value = self.get_hash(key, key_dict)
        self.meta_dict[hash_value] = meta

    def get_hash(self, key: str, key_dict: Dict) -> int:
        for k, v in self.slots.items():
            if v == (key, key_dict):
                return k
        raise KeyError(f"{key}, {key_dict} not found in the registry.")

    def get(self, key: str, key_dict: Dict) -> Any:
        hash_value = self.get_hash(key, key_dict)
        return self.data[hash_value]

    def get_meta(self, key: str, key_dict: Dict) -> Dict:
        hash_value = self.get_hash(key, key_dict)
        return self.meta_dict[hash_value]

    def delete(self, key: str, key_dict: Dict) -> None:
        hash_value = self.get_hash(key, key_dict)
        del self.slots[hash_value]
        del self.data[hash_value]
        del self.meta_dict[hash_value]

    def __contains__(self, key: str, key_dict: Dict) -> bool:
        return (key, key_dict) in self.slots.values()

    def __len__(self) -> int:
        return len(self.slots)

    def __iter__(self):
        return iter(self.slots.values())
