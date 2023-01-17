"""Test cases for Registry sharing.
Author: PeterHartog
"""
import pytest
from abstract_codebase.registration import (
    RegistrationError,
    RegistrationWarning,
    RegistryFactory,
)


class TestSharedRegistry:
    """Test cases for shared Registry class."""

    def test_register(self):
        """Test the register method."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        @TestRegistry.register("shared_registered")
        def test():
            pass

        assert OtherRegistry.get("shared_registered") == test

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        def test():
            pass

        TestRegistry.register_prebuilt(test, "shared_prebuilt")
        assert OtherRegistry.get("shared_prebuilt") == test

    def test_validate_choice_error(self):
        """Test the validate_choice method with an error."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        with pytest.raises(RegistrationError):
            OtherRegistry.validate_choice("shared_unregistered")

    def test_get_error(self):
        """Test the get method with an unregistered key."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        with pytest.raises(RegistrationError):
            OtherRegistry.get("shared_unregistered")

    def test_check_choice_warning(self):
        """Test the register_accreditation method with a warning."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        with pytest.warns(RegistrationWarning):
            OtherRegistry.check_choice("shared_unregistered")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        class TestRegistry(RegistryFactory):
            pass

        class OtherRegistry(RegistryFactory):
            pass

        @TestRegistry.register("double_registered")
        def test():
            pass

        with pytest.raises(KeyError):

            @OtherRegistry.register("double_registered")
            def test2():
                pass
