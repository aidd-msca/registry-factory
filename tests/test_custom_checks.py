"""Test cases for Registry sharing.
Author: PeterHartog
"""
from typing import Any, Dict, Optional, Tuple

import pytest

from registry_factory.factory import Factory
from registry_factory.patterns.observer import RegistryObserver


class TestObservers:
    """Test cases for shared Registry class."""

    class PassiveObserver(RegistryObserver):
        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            return (key, {}, obj, None)

    class RaiseCallError(PassiveObserver):
        def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
            raise ValueError

    class RaiseRegisterError(PassiveObserver):
        def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
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

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[self.RaiseRegisterError()])

        with pytest.raises(Exception):

            @_TestFactory.TestRegistry.register("registered")
            def test():
                pass

    def test_registry_validate_call(self):
        """Test the registry with the validate call method."""

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[self.RaiseCallError()])

        @_TestFactory.TestRegistry.register("registered")
        def test():
            pass

        with pytest.raises(Exception):
            _TestFactory.TestRegistry.get("registered")  # == test

    def test_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class AdditionalError(RegistryObserver):
            def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
                if "test" in kwargs:
                    raise ValueError
                return (key, {}, obj, None)

            def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
                if "test" in kwargs:
                    raise ValueError
                return (key, {}, obj, None)

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, checks=[AdditionalError()])

        with pytest.raises(Exception):

            @_TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(Exception):

            @_TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            _TestFactory.TestRegistry.get("additional_params", test="") == test

    def test_Shared_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class AdditionalError(RegistryObserver):
            def call_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
                if "test" in kwargs:
                    raise ValueError
                return (key, {}, obj, None)

            def register_event(self, key: str, obj: Any, **kwargs) -> Tuple[str, Dict, Any, Optional[Dict]]:
                if "test" in kwargs:
                    raise ValueError
                return (key, {}, obj, None)

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=True, checks=[AdditionalError()])

        with pytest.raises(Exception):

            @_TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(Exception):

            @_TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            _TestFactory.TestRegistry.get("additional_params", test="") == test
