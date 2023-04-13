"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
import pytest

from registry_factory.checks.factory_pattern import FactoryPattern
from registry_factory.factory import Factory


class Pattern:
    """Test pattern."""

    def __init__(self, name):
        self.name = name

    def hello_world(self):
        """Hello world."""
        print("Hello world")


class TestFactoryPattern:
    """Test cases for versioning."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(
            shared=False, checks=[FactoryPattern(factory_pattern=Pattern, forced=False)]
        )
        TestSharedRegistry = Factory.create_registry(
            shared=True, checks=[FactoryPattern(factory_pattern=Pattern, forced=False)]
        )
        ForcedRegistry = Factory.create_registry(
            shared=False, checks=[FactoryPattern(factory_pattern=Pattern, forced=True)]
        )
        ForcedSharedRegistry = Factory.create_registry(
            shared=True, checks=[FactoryPattern(factory_pattern=Pattern, forced=True)]
        )

    def test_pattern(self):
        """Test the pattern."""

        self._TestFactory.TestRegistry.register_prebuilt(key="pattern_test", obj=Pattern)

    def test_wrong_pattern(self):
        """Test the wrong pattern."""

        with pytest.warns():
            self._TestFactory.TestRegistry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")

        with pytest.raises(Exception):
            self._TestFactory.ForcedRegistry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")

    def test_inhereted_pattern(self):
        """Test inhereted pattern."""

        class InheretedPattern(Pattern):
            pass

        class DoubleInheretedPattern(InheretedPattern):
            pass

        self._TestFactory.TestRegistry.register_prebuilt(key="inhereted_test", obj=InheretedPattern)
        self._TestFactory.TestRegistry.register_prebuilt(key="double_inhereted_test", obj=DoubleInheretedPattern)

    def test_wrong_inhereted_pattern(self):
        """Test wrong inhereted pattern."""

        class WrongPattern:
            pass

        with pytest.warns():
            self._TestFactory.TestRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

        with pytest.raises(Exception):
            self._TestFactory.ForcedRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

    def test_common_pattern(self):  # TODO: This shouldn't be a warning, but it is.
        """Test common pattern."""

        class CommonPattern:
            def __init__(self, name):
                self.name = name

            def hello_world(self):
                """Hello world."""
                print("Hello world")

        self._TestFactory.TestRegistry.register_prebuilt(key="common_pattern_test", obj=CommonPattern)

    def test_wrong_common_pattern(self):
        """Test wrong common pattern."""

        class WrongPattern:
            def __init__(self, name):
                self.name = name

            def hello_world2(self):
                """Hello world 2."""
                print("Hello world 2: Electric Boogaloo")

        with pytest.warns():
            self._TestFactory.TestRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)

        with pytest.raises(Exception):
            self._TestFactory.ForcedRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)
