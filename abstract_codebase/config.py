"""Configuration object for dataclasses and yaml."""
import os
import warnings
from abc import ABC, abstractmethod
from dataclasses import _MISSING_TYPE, dataclass, field, fields, make_dataclass
from typing import Any, Dict, List, Optional, Tuple

import yaml
from abstract_codebase import __version__
from abstract_codebase.directories import validate_or_create_file
from abstract_codebase.typescripts import Dataclass

__all__ = ["Config"]


class _ABCHandler(ABC):
    @staticmethod
    @abstractmethod
    def as_config_data(obj: Any) -> Dict[str, Tuple[Any, type]]:
        raise NotImplementedError


class DataclassHandler(_ABCHandler):
    @staticmethod
    def as_config_data(obj: Any) -> Dict[str, Tuple[Any, type]]:
        return {
            f.name: (f.default, f.type) if not isinstance(f.default, _MISSING_TYPE) else (f.default_factory(), f.type)
            for f in fields(obj)
        }

    @staticmethod
    def set_dataclass(dataclass_obj: Any, arguments: Dict[str, Any]) -> Dataclass:
        try:
            dataclass_instance = dataclass_obj(**arguments)
        except Exception:
            raise Exception("Dataclass initiation went wrong." + "Most likely missing field values in config.")
        return dataclass_instance

    @staticmethod
    def get_dataclass(call_name: str, obj: Dict[str, Any]) -> Dataclass:
        """Returns arguments of a argument class as a new dataclass."""

        def choose_field(key: str, field_value: Any) -> Tuple:
            if isinstance(field_value, (Dict, List)):
                return (
                    key,
                    "typing.Any",
                    field(default_factory=lambda: field_value),
                )
            elif field_value is not None:
                return (key, "typing.Any", field(default=field_value))
            else:
                return (key, "typing.Optional", None)

        dataclass_fields = [choose_field(key, field_value) for key, field_value in obj.items()]
        new_dataclass = make_dataclass(call_name, dataclass_fields)
        return new_dataclass()


class YamlHandler(_ABCHandler):
    @staticmethod
    def as_config_data(obj: Any) -> Dict[str, Tuple[Any, type]]:
        if isinstance(obj, Dict):
            return {key: (value, type(value)) for key, value in obj.items()}
        else:
            return (obj, type(obj))

    @staticmethod
    def read_yaml(file: str) -> Dict:
        with open(file) as file:
            yaml_config = yaml.safe_load(file)
        return yaml_config

    @staticmethod
    def dict_to_yaml(file: str, obj: Dict) -> None:
        with open(validate_or_create_file(file), "w") as outfile:
            yaml.dump(obj, outfile, default_flow_style=False)


# Command Line Interface (CLI) Handler for the config file
# Untested copilot implementation
class CLIHandler:
    @staticmethod
    def as_config_data(obj: Any) -> Dict[str, Tuple[Any, type]]:
        if isinstance(obj, Dict):
            return {key: (value, type(value)) for key, value in obj.items()}
        else:
            return (obj, type(obj))

    @staticmethod
    def get_cli_arguments() -> Dict[str, Any]:
        """Returns the command line arguments."""
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--config", "-c", help="Path to the config file.")
        parser.add_argument("--version", "-v", action="store_true", help="Prints the version of the codebase.")
        args = parser.parse_args()
        return vars(args)


@dataclass(unsafe_hash=True)
class Config:
    codebase_version: str = __version__
    config_data: Dict[str, Dict[str, Tuple[Any, type]]] = field(default_factory=lambda: {})
    data_classes: Dict[str, Dataclass] = field(default_factory=lambda: {})

    def to_environment(self, key: str, value: Any):
        self.__dict__[key] = value[0]

    def to_config_data(self, group_name: str, obj: Any, handler: _ABCHandler) -> None:
        self.config_data[group_name] = handler.as_config_data(obj)

    def overwrite_config_data(self, group_name: str, obj: Any, handler: _ABCHandler) -> None:
        obj_data = handler.as_config_data(obj)
        for k, (v, t) in obj_data.items():
            if k in self.config_data[group_name].keys():
                if t == self.config_data[group_name][k][1]:
                    self.config_data[group_name][k] = (v, t)
                else:
                    warnings.warn(f"Key {k} type not matching original.")
                    self.config_data[group_name][k] = (v, t)
            else:
                warnings.warn(f"Key {k} not found in original.")
                self.config_data[group_name][k] = (v, t)

    def processing_arguments(self, group: str, obj: Any, handler: _ABCHandler) -> None:
        obj_data = handler.as_config_data(obj)
        if isinstance(obj_data, Dict) and group != "env":
            if group in self.config_data.keys():
                self.overwrite_config_data(group, obj, handler)
            else:
                self.to_config_data(group, obj, handler)
        else:
            if isinstance(obj_data, Dict):
                for k, v in obj_data.items():
                    self.to_environment(k, v)
            else:
                self.to_environment(group, obj_data)

    def dataclass_override(self, data_classes: Dict[str, Dataclass]) -> None:
        """Overrides the config with dataclass objects."""
        for group, data_object in data_classes.items():
            self.processing_arguments(group, data_object, DataclassHandler)

    def yaml_override(self, file: str) -> None:
        """Overrides the config with yaml file objects."""
        if os.path.exists(file) and YamlHandler.read_yaml(file):
            yaml_object = YamlHandler.read_yaml(file)
            for group, data_object in yaml_object.items():
                self.processing_arguments(group, data_object, YamlHandler)
        else:
            warnings.warn("yaml file not found.")

    def return_self(self) -> Dict[str, Any]:
        """Returns the config as a dictionary."""
        self_dict = {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("__") and key not in ["data_classes"]
        }
        return self_dict

    def return_arguments(self, call_name: str) -> Dict[str, Any]:
        """Returns current configuration of a call_name as a dictionary."""
        return {k: v for k, (v, _) in self.config_data[call_name].items()}

    def return_dataclass(self, call_name: str) -> Dataclass:
        """Returns current configuration of a call_name as a dataclass."""
        if call_name in self.data_classes.keys():
            return DataclassHandler.set_dataclass(self.data_classes[call_name], self.return_arguments(call_name))
        else:
            return DataclassHandler.get_dataclass(call_name, self.return_arguments(call_name))

    def print_arguments(self) -> None:
        """Prints all arguments in the config."""
        self_dict = self.return_self()
        for k, v in self_dict.items():
            if k != "config_data":
                print(f"Arg {k} = {v}")
        for ki, vi in self.config_data.items():
            print(f"\n=={ki}==")
            for kij, (vij, _) in vi.items():
                print(f"Arg {kij} = {vij}")

    def generate_yaml(self, file_location: str, call_name: Optional[str] = None) -> None:
        """Generates a YAML file with the current configuration."""
        if call_name:
            YamlHandler.dict_to_yaml(file_location, self.return_arguments(call_name))
        else:
            self_dict = {k: v for k, v in self.return_self().items() if k != "config_data"}
            for key in self.config_data.keys():
                self_dict[key] = self.return_arguments(key)
            YamlHandler.dict_to_yaml(file_location, self_dict)
