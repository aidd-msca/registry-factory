"""Test cases for Registry arguments.
Author: PeterHartog
"""
import pytest
from registry_factory.utils import RegistrationError, RegistrationWarning
from registry_factory.factory import Factory
from dataclasses import dataclass


class TestArgumentsRegistry:
    """Test cases for a arguments from created Registry class."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=False)

    def test_register_arguments(self):
        """Test the register_arguments method."""

        @self._TestFactory.TestRegistry.register_arguments("registered")
        @dataclass
        class Test:
            arg1 = 1

        assert self._TestFactory.TestRegistry.get_arguments("registered") == Test

    def test_register_arguments_not_dataclass(self):
        """Test the register_arguments method with a non dataclass."""

        with pytest.raises(RegistrationError):

            @self._TestFactory.TestRegistry.register_arguments("registered_non_dataclass")
            def test():
                pass

    def test_register_arguments_not_dataclass_warning(self):
        """Test the register_arguments method with a non dataclass and a warning."""
        with pytest.warns(RegistrationWarning):

            @self._TestFactory.TestRegistry.register_arguments("registered_non_dataclass")
            class Test:
                arg1 = 1

    def test_register_arguments_already_registered(self):
        """Test the register_arguments method with a already registered key."""

        with pytest.raises(KeyError):

            @self._TestFactory.TestRegistry.register_arguments("registered")
            @dataclass
            class Test:
                arg1 = 1
