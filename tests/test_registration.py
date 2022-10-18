"""Test cases for the registration module.
Author: all hail Github Copilot (untested)
"""
import pytest
from abstract_codebase.accreditation import CreditInfo, CreditType
from abstract_codebase.registration import (
    RegistrationError,
    RegistrationWarning,
    RegistryFactory,
)


class TestRegistryFactory:
    """Test cases for the RegistryFactory class."""

    def test_call(self):
        """Test the __call__ method."""
        registry = RegistryFactory()
        registry.index["test"] = "test"
        assert registry("test") == "test"

    def test_getitem(self):
        """Test the __getitem__ method."""
        registry = RegistryFactory()
        registry.index["test"] = "test"
        assert registry["test"] == "test"

    def test_contains(self):
        """Test the __contains__ method."""
        registry = RegistryFactory()
        registry.index["test"] = "test"
        assert "test" in registry

    def test_len(self):
        """Test the __len__ method."""
        registry = RegistryFactory()
        registry.index["test"] = "test"
        assert len(registry) == 1

    def test_iter(self):
        """Test the __iter__ method."""
        registry = RegistryFactory()
        registry.index["test"] = "test"
        assert list(registry) == ["test"]

    def test_register(self):
        """Test the register method."""
        registry = RegistryFactory()
        registry.register("test")("test")
        assert registry.index["test"] == "test"

    def test_register_prebuilt(self):
        """Test the register prebuilt method."""
        registry = RegistryFactory()
        registry.register_prebuilt("test", "test")
        assert registry.index["test"] == "test"

    def test_register_accreditation(self):
        """Test the register_accreditation method."""
        registry = RegistryFactory()
        registry.register_prebuilt("test", "test")
        registry.get("test")
        assert registry.accreditation.called_objects == {"test"}

    def test_validate_choice_error(self):
        """Test the register_accreditation method with an error."""
        registry = RegistryFactory()
        with pytest.raises(RegistrationError):
            registry.validate_choice("test")

    def test_check_choice_warning(self):
        """Test the register_accreditation method with a warning."""
        registry = RegistryFactory()
        with pytest.warns(RegistrationWarning):
            registry.check_choice("test")

    def test_registry_factory_prebuilt(self):
        """Test the RegistryFactory class with prebuilt objects."""
        # Create a registry
        registry = RegistryFactory("test_registry")
        assert registry == RegistryFactory["test_registry"]
        assert "test_registry" in RegistryFactory
        assert len(RegistryFactory) == 1
        assert list(RegistryFactory) == ["test_registry"]
        assert registry.accreditation == RegistryFactory.accreditation

        # Register a function
        registry.register_prebuilt("test_function", "test_function")
        assert registry["test_function"] == "test_function"
        assert registry("test_function") == "test_function"
        assert registry.accreditation["test_function"] == CreditInfo("test_function", CreditType.function)

        # Register a class
        registry.register_prebuilt("TestClass", "TestClass")
        assert registry["TestClass"] == "TestClass"
        assert registry("TestClass") == "TestClass"
        assert registry.accreditation["TestClass"] == CreditInfo("TestClass", CreditType.class_)

        # Register a class instance
        registry.register_prebuilt("test_instance", "test_instance")
        assert registry["test_instance"] == "test_instance"
        assert registry("test_instance") == "test_instance"
        assert registry.accreditation["test_instance"] == CreditInfo("test_instance", CreditType.instance)

        # Register a class method
        registry.register_prebuilt("test_class_method", "test_class_method")
        assert registry["test_class_method"] == "test_class_method"
        assert registry("test_class_method") == "test_class_method"
        assert registry.accreditation["test_class_method"] == CreditInfo("test_class_method", CreditType.class_method)

    def test_registry_factory(self):
        """Test the RegistryFactory class."""
        # Create a registry
        registry = RegistryFactory("test_registry")
        assert registry == RegistryFactory["test_registry"]
        assert "test_registry" in RegistryFactory
        assert len(RegistryFactory) == 1
        assert list(RegistryFactory) == ["test_registry"]
        assert registry.accreditation == RegistryFactory.accreditation

        # Register a function
        @registry.register("test_function")
        def test_function():
            """Test function."""
            return "test_function"

        assert registry["test_function"] == test_function
        assert registry("test_function") == test_function
        assert registry.accreditation["test_function"] == CreditInfo("test_function", CreditType.function)

        # Register a class
        @registry.register("TestClass")
        class TestClass:
            """Test class."""

            def __init__(self):
                """Initialize the TestClass."""
                self.test_class = "test_class"

        assert registry["TestClass"] == TestClass
        assert registry("TestClass") == TestClass
        assert registry.accreditation["TestClass"] == CreditInfo("TestClass", CreditType.class_)

        # Register a class instance
        @registry.register("test_instance")
        class TestInstance:
            """Test instance."""

            def __init__(self):
                """Initialize the TestInstance."""
                self.test_instance = "test_instance"

        assert registry["test_instance"] == TestInstance()
        assert registry("test_instance") == TestInstance()
        assert registry.accreditation["test_instance"] == CreditInfo("test_instance", CreditType.instance)

        # Register a class method
        @registry.register("test_class_method")
        class TestClassMethod:
            """Test class method."""

            def __init__(self):
                """Initialize the TestClassMethod."""
                self.test_class_method = "test_class_method"

            @classmethod
            def test_class_method(cls):
                """Test class method."""
                return cls().test_class_method

        assert registry["test_class_method"] == TestClassMethod.test_class_method
        assert registry("test_class_method") == TestClassMethod.test_class_method
        assert registry.accreditation["test_class_method"] == CreditInfo("test_class_method", CreditType.class_method)

