"""Test cases for Registry not sharing.
Author: PeterHartog
"""

import pytest
from abstract_codebase.registration import RegistrationError, Factory


class TestUnsharedRegistry:
    """Test cases for shared Registry class."""

    class TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=True)
        TestUnsharedRegistry = Factory.create_registry(shared=False)

    def test_register(self):
        """Test the register method."""

        @self.TestFactory.TestRegistry.register("unshared_registered")
        def test():
            pass

        with pytest.raises(RegistrationError):
            self.TestFactory.TestUnsharedRegistry.get("unshared_registered")

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""

        def test():
            pass

        self.TestFactory.TestRegistry.register_prebuilt(test, "unshared_prebuilt")
        with pytest.raises(RegistrationError):
            self.TestFactory.TestUnsharedRegistry.get("unshared_prebuilt")

    def test_shared_double_register(self):
        """Test the register method with a double registration."""

        @self.TestFactory.TestRegistry.register("unshared_double_registered")
        def test():
            pass

        def test2():
            pass

        self.TestFactory.TestRegistry.register_prebuilt(test2, "unshared_double_prebuilt")

        @self.TestFactory.TestUnsharedRegistry.register("unshared_double_registered")
        def test3():
            pass

        @self.TestFactory.TestUnsharedRegistry.register("unshared_double_prebuilt")
        def test4():
            pass
