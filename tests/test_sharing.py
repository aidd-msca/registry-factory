"""Test cases for Registry sharing.
Author: PeterHartog
"""
from abstract_codebase.metacoding import UniqueDict
import pytest
from abstract_codebase.registration import (
    RegistrationError,
    RegistrationWarning,
    RegistryFactory,
)


class TestSharedRegistry:
    """Test cases for shared Registry class."""

    class TestRegistry(RegistryFactory):
        pass

    class TestSharedRegistry(RegistryFactory):
        pass

    def test_register(self):
        """Test the register method."""

        @self.TestRegistry.register("shared_registered")
        def test():
            pass

        assert self.TestSharedRegistry.get("shared_registered") == test

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self.TestRegistry.register_prebuilt(test, "shared_prebuilt")
        assert self.TestSharedRegistry.get("shared_prebuilt") == test

    def test_validate_choice_error(self):
        """Test the validate_choice method with an error."""

        with pytest.raises(RegistrationError):
            self.TestSharedRegistry.validate_choice("shared_unregistered")

    def test_get_error(self):
        """Test the get method with an unregistered key."""

        with pytest.raises(RegistrationError):
            self.TestSharedRegistry.get("shared_unregistered")

    def test_check_choice_warning(self):
        """Test the register_accreditation method with a warning."""

        with pytest.warns(RegistrationWarning):
            self.TestSharedRegistry.check_choice("shared_unregistered")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        @self.TestRegistry.register("shared_double_registered")
        def test():
            pass

        with pytest.raises(KeyError):

            @self.TestSharedRegistry.register("shared_double_registered")
            def test2():
                pass


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
