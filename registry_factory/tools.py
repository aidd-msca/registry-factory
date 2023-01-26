"""Generic helper tools."""
import functools
from typing import Any, Callable, Dict, List

__all__ = ["omit_from_dict", "compose", "convert_dict_names_to_lower", "convert_dict_names_to_upper"]


def omit_from_dict(dict: Dict, omit_keys: List[str]) -> Dict:
    return {k: v for k, v in dict.items() if k not in omit_keys}


def compose(*functions: Callable) -> Callable:
    """Helper function to compose together sequential operations."""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)


def convert_dict_names_to_lower(dict: Dict[str, Any]) -> Dict[str, Any]:
    return {k.lower(): v for k, v in dict.items()}


def convert_dict_names_to_upper(dict: Dict[str, Any]) -> Dict[str, Any]:
    return {k.upper(): v for k, v in dict.items()}
