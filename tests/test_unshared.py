"""Test cases for Registry not sharing.
Author: PeterHartog
"""

import pytest
from registry_factory.registration import RegistrationError
from registry_factory.factory import Factory


class TestUnsharedRegistry:
    """Test cases for shared Registry class."""

    # @pytest.mark.skip(reason="Not a test, just a helper.")
    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=True)
        TestUnsharedRegistry = Factory.create_registry(shared=False)

    def test_register(self):
        """Test the register method."""

        @self._TestFactory.TestRegistry.register("unshared_registered")
        def test():
            pass

        with pytest.raises(RegistrationError):
            self._TestFactory.TestUnsharedRegistry.get("unshared_registered")

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self._TestFactory.TestRegistry.register_prebuilt(test, "unshared_prebuilt")
        with pytest.raises(RegistrationError):
            self._TestFactory.TestUnsharedRegistry.get("unshared_prebuilt")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        @self._TestFactory.TestRegistry.register("unshared_double_registered")
        def test():
            pass

        def test2():
            pass

        self._TestFactory.TestRegistry.register_prebuilt(test2, "unshared_double_prebuilt")

        @self._TestFactory.TestUnsharedRegistry.register("unshared_double_registered")
        def test3():
            pass

        @self._TestFactory.TestUnsharedRegistry.register("unshared_double_prebuilt")
        def test4():
            pass
