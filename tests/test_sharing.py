"""Test cases for Registry sharing.
Author: PeterHartog
"""
import pytest

from registry_factory.factory import Factory
from registry_factory.utils import RegistrationError, RegistrationWarning


class TestSharedRegistry:
    """Test cases for shared Registry class."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=True)
        TestSharedRegistry = Factory.create_registry(shared=True)

    def test_register(self):
        """Test the register method."""

        @self._TestFactory.TestRegistry.register("shared_registered")
        def test():
            pass

        assert self._TestFactory.TestRegistry.get("shared_registered") == test

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self._TestFactory.TestRegistry.register_prebuilt(test, "shared_prebuilt")
        assert self._TestFactory.TestSharedRegistry.get("shared_prebuilt") == test

    def test_validate_choice_error(self):
        """Test the validate_choice method with an error."""

        with pytest.raises(RegistrationError):
            self._TestFactory.TestSharedRegistry.validate_choice("shared_unregistered")

    def test_get_error(self):
        """Test the get method with an unregistered key."""

        with pytest.raises(RegistrationError):
            self._TestFactory.TestSharedRegistry.get("shared_unregistered")

    def test_check_choice_warning(self):
        """Test the register_accreditation method with a warning."""

        with pytest.warns(RegistrationWarning):
            self._TestFactory.TestSharedRegistry.check_choice("shared_unregistered")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        @self._TestFactory.TestRegistry.register("shared_double_registered")
        def test():
            pass

        with pytest.raises(KeyError):

            @self._TestFactory.TestSharedRegistry.register("shared_double_registered")
            def test2():
                pass
