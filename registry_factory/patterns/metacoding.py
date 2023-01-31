"""Metacoding classes to aid codebase design."""
from collections import defaultdict
from typing import Dict, List

__all__ = ["Singleton", "Borg", "Final", "UniqueDict", "MetaRegistry", "ReducedClass", "InheretanceTracker"]


class Singleton:
    """Only allows one instance to exist, new instances get overridden."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)  # , *args, **kwargs)
        return cls._instance


class Borg:
    """Shared self dictionary between instances."""

    _dict = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        if cls._dict is None:
            cls._dict = obj.__dict__
        else:
            obj.__dict__ = cls._dict
        return obj


class Final:
    """Raises error when inherited."""

    def __init__(cls, name, bases, namespace):
        super(Final, cls).__init__(name, bases, namespace)
        for klass in bases:
            if isinstance(klass, Final):
                raise TypeError(str(klass.__name__) + " is final")


class UniqueDict(dict):
    """Dict that raises when reassigning an existing key."""

    def __setitem__(self, key, value):
        if self.__contains__(key):
            raise KeyError("Key already in dict.")
        else:
            super().__setitem__(key, value)


class MetaRegistry:
    """Registry using decorators."""

    index: Dict[str, object] = UniqueDict()

    @classmethod
    def register(cls, call_name: str) -> object:
        """Registers an object to a key using a decorator."""

        def wrapper(obj: object) -> object:
            cls.index[call_name] = obj
            return obj

        return wrapper


class ReducedClass:
    """Reduces class state to base class and self.__dict__."""

    def __reduce__(self):
        state = self.__dict__.copy()
        return (_NestedClassGetter(), (ReducedClass, self.__class__.__name__), state)


class _NestedClassGetter(object):
    """When called with the containing class and the name of the nested class,
    returns an instance of the nested class.
    """

    def __call__(self, containing_class, class_name):
        nested_class = getattr(containing_class, class_name)
        nested_instance = _NestedClassGetter()
        nested_instance.__class__ = nested_class
        return nested_instance


class InheretanceTracker(object):
    """Class that tracks inheretance in a set."""

    class __metaclass__(type):
        __inheritors__: Dict[str, List] = defaultdict(list)

        def __new__(meta, name, bases, dct):
            klass = type.__new__(meta, name, bases, dct)
            for base in klass.mro()[1:-1]:
                meta.__inheritors__[base].append(klass)
            return klass
