from typing import Any, Dict, Optional, Tuple
import warnings
from registry_factory.patterns.metacoding import UniqueDict
import random

from registry_factory.typescripts import Dataclass


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


class AbstractHash:
    """Abstract class for hash table."""

    slots: Dict[int, Any]
    data: Dict[int, Any]

    def __init__(self, bitsize: int = 256, max_generation: int = 1000):
        self.bitsize = bitsize
        self.max_generation = max_generation
        self.slots = {}
        self.data = {}

    def generate_hash(self) -> int:
        key_hash = random.getrandbits(self.bitsize)

        current_generation = 0
        while key_hash in self.slots and current_generation < self.max_generation:
            key_hash = self.generate_hash()
            current_generation += 1

        return key_hash

    def __len__(self) -> int:
        return len(self.slots)

    def __iter__(self):
        return iter(self.slots.values())


class HashTable(AbstractHash):
    """Hash table."""

    slots: Dict[int, Tuple[str, Dict]]
    data: Dict[int, Any]
    arg_dict: Dict[int, Dataclass]
    meta_dict: Dict[int, Dict]

    def __init__(self, bitsize: int = 256, max_generation: int = 1000):
        super().__init__(bitsize, max_generation)
        self.meta_dict = {}

    def set(self, key: str, key_dict: Dict, obj: Any, meta: Optional[Dict] = None) -> None:
        full_key: Tuple[str, Dict] = (key, key_dict)
        if full_key in self.slots.values():
            hash_value = self.get_hash(key, key_dict)
            if hash_value in self.data.keys():
                raise KeyError(f"{key}, {key_dict} already exist in the registry.")
        else:
            hash_value = self.generate_hash()
            self.slots[hash_value] = full_key
        self.data[hash_value] = obj
        if meta is not None:
            self.meta_dict[hash_value] = meta

    def set_arguments(self, key: str, key_dict: Dict, arguments: Dataclass) -> None:
        full_key: Tuple[str, Dict] = (key, key_dict)
        if full_key in self.slots.values() and full_key in self.arg_dict.values():
            raise KeyError(f"{key}, {key_dict} arguments already exist in the registry.")
        elif full_key in self.slots.values():
            hash_value = self.get_hash(key, key_dict)
        else:
            hash_value = self.generate_hash()
            self.slots[hash_value] = full_key
        self.arg_dict[hash_value] = arguments

    def get_hash(self, key: str, key_dict: Dict) -> int:
        for k, v in self.slots.items():
            if v == (key, key_dict):
                return k
        raise KeyError(f"{key}, {key_dict} not found in the registry.")

    def get(self, key: str, key_dict: Dict) -> Any:
        hash_value = self.get_hash(key, key_dict)
        return self.data[hash_value]

    def get_arguments(self, key: str, key_dict: Dict) -> Dataclass:
        hash_value = self.get_hash(key, key_dict)
        return self.arg_dict[hash_value]

    def get_meta(self, key: str, key_dict: Dict) -> Dict:
        hash_value = self.get_hash(key, key_dict)
        return self.meta_dict[hash_value]

    def delete(self, key: str, key_dict: Dict) -> None:
        hash_value = self.get_hash(key, key_dict)
        del self.slots[hash_value]
        del self.data[hash_value]
        del self.meta_dict[hash_value]

    def clear(self) -> None:
        self.slots.clear()
        self.data.clear()
        self.meta_dict.clear()

    def __contains__(self, key: str, key_dict: Dict) -> bool:
        return (key, key_dict) in self.slots.values()


class RegistryTable(AbstractHash):
    slots: Dict[int, Any]

    def set(self, hash: Optional[int] = None) -> None:
        if hash is None:
            hash = self.generate_hash()
        elif hash in self.slots.keys():
            raise KeyError(f"{hash} already exists.")

        self.slots[hash] = HashTable()

    def get_hash(self, hash: int) -> int:
        for k, v in self.slots.items():
            if k == hash:
                return v
        raise KeyError(f"{hash} not found.")

    def get(self, hash: int) -> HashTable:
        hash_value = self.get_hash(hash)
        return self.data[hash_value]

    def get_meta(self, **kwargs) -> Dict:
        raise NotImplementedError

    def delete(self, hash: int) -> None:
        del self.slots[hash]

    def __contains__(self, hash: int) -> bool:
        return hash in self.slots.keys()
