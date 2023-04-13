"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
from typing import Any

import pytest

from registry_factory.checks.testing import Testing as _Testing
from registry_factory.factory import Factory


class CallableTestModule:
    """Module to test."""

    def __init__(self, key: str, obj: Any, **kwargs):
        self.name = obj
        self.assert_name()

    def assert_name(self):
        assert self.name == "test", "Name is not test"


class TestFactoryPattern:
    """Test cases for versioning."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(
            shared=False, checks=[_Testing(test_module=CallableTestModule, forced=False)]
        )
        TestSharedRegistry = Factory.create_registry(
            shared=True, checks=[_Testing(test_module=CallableTestModule, forced=False)]
        )
        ForcedRegistry = Factory.create_registry(
            shared=False, checks=[_Testing(test_module=CallableTestModule, forced=True)]
        )
        ForcedSharedRegistry = Factory.create_registry(
            shared=True, checks=[_Testing(test_module=CallableTestModule, forced=True)]
        )

    def test_testing(self):
        """Test the _Testing."""

        self._TestFactory.TestRegistry.register_prebuilt(key="name_test", obj="test")

    def test_wrong_pattern(self):
        """Test the wrong pattern."""

        with pytest.warns():
            self._TestFactory.TestRegistry.register_prebuilt(key="wrong_name_test", obj="not_test")

        with pytest.raises(Exception):
            self._TestFactory.ForcedRegistry.register_prebuilt(key="wrong_name_test", obj="not_test")
