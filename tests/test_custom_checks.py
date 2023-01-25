"""Test cases for Registry sharing.
Author: PeterHartog
"""
from typing import Any
import pytest

from abstract_codebase.patterns.observer import RegistryObserver
from abstract_codebase.factory import Factory


class TestObservers:
    """Test cases for shared Registry class."""

    class Test(Factory):
        TestRegistry = Factory.create_registry(shared=True, checks=[])
        ForcedCreditRegistry = Factory.create_registry(shared=True, checks=[])

    class PassiveObserver(RegistryObserver):
        def register_event(self, key: str, object: Any, **kwargs):
            pass

        def call_event(self, key: str, **kwargs):
            pass

        def print_info(self, key: str) -> str:
            pass

    class RaiseCallError(PassiveObserver):
        def call_event(self, key: str, **kwargs):
            raise ValueError

    class RaiseRegisterError(PassiveObserver):
        def register_event(self, key: str, object: Any, **kwargs):
            raise ValueError

    def test_instantiation(self):
        """Test creating a new method with the abstract methods."""
        self.PassiveObserver()

    def test_wrong_instantiation(self):
        """Test creating a new method without the abstract methods."""

        class TestCustomCheck(RegistryObserver):
            pass

        with pytest.raises(TypeError):
            TestCustomCheck()

    def test_registry_validate_register(self):
        """Test the registry with the validate register method."""

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[self.RaiseRegisterError()])

        with pytest.raises(Exception):

            @TestFactory.TestRegistry.register("registered")
            def test():
                pass

    def test_registry_validate_call(self):
        """Test the registry with the validate call method."""

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[self.RaiseCallError()])

        @TestFactory.TestRegistry.register("registered")
        def test():
            pass

        with pytest.raises(Exception):
            TestFactory.TestRegistry.get("registered")  # == test

    def test_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class AdditionalError(RegistryObserver):
            def call_event(self, key: str, **kwargs):
                if "test" in kwargs:
                    raise ValueError

            def register_event(self, key: str, object: Any, **kwargs):
                if "test" in kwargs:
                    raise ValueError

            def print_info(self, key: str) -> str:
                pass

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[AdditionalError()])

        with pytest.raises(Exception):

            @TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(Exception):

            @TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            TestFactory.TestRegistry.get("additional_params", test="") == test

    def test_Shared_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class AdditionalError(RegistryObserver):
            def call_event(self, key: str, **kwargs):
                if "test" in kwargs:
                    raise ValueError

            def register_event(self, key: str, object: Any, **kwargs):
                if "test" in kwargs:
                    raise ValueError

            def print_info(self, key: str) -> str:
                pass

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=True, checks=[AdditionalError()])

        with pytest.raises(Exception):

            @TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(Exception):

            @TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            TestFactory.TestRegistry.get("additional_params", test="") == test
