"""Test cases for Registry registration.
Author: PeterHartog
"""
import pytest
from registry_factory.registration import AbstractRegistry, RegistrationError, RegistrationWarning
from registry_factory.factory import Factory


class TestIndividualRegistry:
    """Test cases for a newly created Registry class."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=True)

    def test_inheritance(self):
        """Test the inheritance of the Registry class."""

        assert issubclass(self._TestFactory.TestRegistry, AbstractRegistry)

    def test_register(self):
        """Test the register method."""

        @self._TestFactory.TestRegistry.register("registered")
        def test():
            pass

        assert self._TestFactory.TestRegistry.get("registered") == test

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self._TestFactory.TestRegistry.register_prebuilt(test, "prebuilt")
        assert self._TestFactory.TestRegistry.get("prebuilt") == test

    def test_validate_choice_error(self):
        """Test the validate_choice method with an error."""

        with pytest.raises(RegistrationError):
            self._TestFactory.TestRegistry.validate_choice("unregistered")

    def test_get_error(self):
        """Test the get method with an unregistered key."""

        with pytest.raises(RegistrationError):
            self._TestFactory.TestRegistry.get("unregistered")

    def test_check_choice_warning(self):
        """Test the register_accreditation method with a warning."""

        with pytest.warns(RegistrationWarning):
            self._TestFactory.TestRegistry.check_choice("unregistered")

    def test_double_register(self):
        """Test the register method with a double registration."""

        @self._TestFactory.TestRegistry.register("double_registered")
        def registered_object():
            pass

        def prebuilt_object():
            pass

        self._TestFactory.TestRegistry.register_prebuilt(prebuilt_object, "double_prebuilt")

        with pytest.raises(KeyError):

            @self._TestFactory.TestRegistry.register("double_registered")
            def test1():
                pass

        with pytest.raises(KeyError):

            @self._TestFactory.TestRegistry.register("double_prebuilt")
            def test2():
                pass

        with pytest.raises(KeyError):

            def test3():
                pass

            self._TestFactory.TestRegistry.register_prebuilt(test3, "double_registered")

        with pytest.raises(KeyError):

            def test4():
                pass

            self._TestFactory.TestRegistry.register_prebuilt(test4, "double_prebuilt")
