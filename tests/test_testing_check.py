"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
import pytest
from registry_factory.checks.testing import Testing
from registry_factory.factory import Factory


class CallableTestModule:
    """Module to test."""

    def __init__(self, name):
        self.name = name
        self.assert_name()

    def assert_name(self):
        assert self.name == "test", "Name is not test"


class TestFactoryPattern:
    """Test cases for versioning."""

    class TestFactory(Factory):
        TestRegistry = Factory.create_registry(
            shared=False, checks=[Testing(test_module=CallableTestModule, forced=False)]
        )
        TestSharedRegistry = Factory.create_registry(
            shared=True, checks=[Testing(test_module=CallableTestModule, forced=False)]
        )
        ForcedRegistry = Factory.create_registry(
            shared=False, checks=[Testing(test_module=CallableTestModule, forced=True)]
        )
        ForcedSharedRegistry = Factory.create_registry(
            shared=True, checks=[Testing(test_module=CallableTestModule, forced=True)]
        )

    def test_testing(self):
        """Test the testing."""

        self.TestFactory.TestRegistry.register_prebuilt(key="name_test", obj="test")

    def test_wrong_pattern(self):
        """Test the wrong pattern."""

        with pytest.warns():
            self.TestFactory.TestRegistry.register_prebuilt(key="wrong_name_test", obj="not_test")

        with pytest.raises(Exception):
            self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_name_test", obj="not_test")

    # def test_inhereted_pattern(self):
    #     """Test inhereted pattern."""

    #     class InheretedPattern(Pattern):
    #         pass

    #     class DoubleInheretedPattern(InheretedPattern):
    #         pass

    #     self.TestFactory.TestRegistry.register_prebuilt(key="inhereted_test", obj=InheretedPattern)
    #     self.TestFactory.TestRegistry.register_prebuilt(key="double_inhereted_test", obj=DoubleInheretedPattern)

    # def test_wrong_inhereted_pattern(self):
    #     """Test wrong inhereted pattern."""

    #     class WrongPattern:
    #         pass

    #     with pytest.warns():
    #         self.TestFactory.TestRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

    #     with pytest.raises(Exception):
    #         self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

    # def test_common_pattern(self):  # TODO: This shouldn't be a warning, but it is.
    #     """Test common pattern."""

    #     class CommonPattern:
    #         def __init__(self, name):
    #             self.name = name

    #         def hello_world(self):
    #             """Hello world."""
    #             print("Hello world")

    #     self.TestFactory.TestRegistry.register_prebuilt(key="common_pattern_test", obj=CommonPattern)

    # def test_wrong_common_pattern(self):
    #     """Test wrong common pattern."""

    #     class WrongPattern:
    #         def __init__(self, name):
    #             self.name = name

    #         def hello_world2(self):
    #             """Hello world 2."""
    #             print("Hello world 2: Electric Boogaloo")

    #     with pytest.warns():
    #         self.TestFactory.TestRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)

    #     with pytest.raises(Exception):
    #         self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)
