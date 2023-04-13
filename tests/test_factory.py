"""Test cases for Registry sharing.
Author: PeterHartog
"""
import pytest

from registry_factory.factory import Factory


class TestFactory:
    """Test cases for Registry Factory."""

    def test_instantiation(self):
        """Test creating a new method with the abstract methods."""

        with pytest.raises(ValueError):
            Factory()

    def test_inheretence(self):
        """Test creating a new method without the abstract methods."""

        class _TestFactory(Factory):
            pass

    def test_create_registry(self):
        """Test creating a new registry."""

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry()

        assert _TestFactory.TestRegistry is not None

    def test_create_shared_registry(self):
        """Test creating a new shared registry."""

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=True)

        assert _TestFactory.TestRegistry is not None

    def test_create_registry_from_self(self):
        """Test creating a new registry from self."""

        with pytest.raises(AttributeError):

            class _TestFactory(Factory):
                TestRegistry = self.create_registry()

    def test_get_registries(self):
        """Test getting all registries."""

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry()

        assert "TestRegistry" in _TestFactory.get_registries().keys()

    def test_get_subclass_choices(self):
        """Test getting the subclass choices."""

        class _TestFactory(Factory):
            TestRegistry = Factory.create_registry()

        @_TestFactory.TestRegistry.register("test")
        def test():
            pass

        print(Factory)
        import os

        dir_path = os.path.dirname(os.path.realpath(Factory))
        print(dir_path)

        assert ("test", {}) in _TestFactory.items()

    # def test_get_subclass_arguments(self):
    #     """Test getting the subclass choices."""

    #     class _TestFactory(Factory):
    #         TestRegistry = Factory.create_registry()

    #     @_TestFactory.TestRegistry.register_arguments("test_arg")
    #     @dataclass
    #     class TestArguments:
    #         test_arg: str

    #     assert TestArguments in _TestFactory.get_registry_arguments(["TestRegistry"]).values()
