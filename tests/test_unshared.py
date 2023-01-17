"""Test cases for Registry not sharing.
Author: PeterHartog
"""
from abstract_codebase.metacoding import UniqueDict
import pytest
from abstract_codebase.registration import (
    RegistrationError,
    RegistryFactory,
)


class TestUnsharedRegistry:
    """Test cases for shared Registry class."""

    class TestRegistry(RegistryFactory):
        pass

    class TestUnsharedRegistry(RegistryFactory):
        index: UniqueDict = UniqueDict()

    def test_register(self):
        """Test the register method."""

        @self.TestRegistry.register("unshared_registered")
        def test():
            pass

        with pytest.raises(RegistrationError):
            self.TestUnsharedRegistry.get("unshared_registered")

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self.TestRegistry.register_prebuilt(test, "unshared_prebuilt")
        with pytest.raises(RegistrationError):
            self.TestUnsharedRegistry.get("unshared_prebuilt")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        @self.TestRegistry.register("unshared_double_registered")
        def test():
            pass

        def test2():
            pass

        self.TestRegistry.register_prebuilt(test2, "unshared_double_prebuilt")

        @self.TestUnsharedRegistry.register("unshared_double_registered")
        def test3():
            pass

        @self.TestUnsharedRegistry.register("unshared_double_prebuilt")
        def test4():
            pass
