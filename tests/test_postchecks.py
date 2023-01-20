"""Test cases for Registry sharing.
Author: PeterHartog
"""
from typing import Any
from abstract_codebase.index import IndexDict
from abstract_codebase.postchecks import AbstractPostCheck
import pytest
from abstract_codebase.registration import Factory


class TestPostCheck:
    """Test cases for shared Registry class."""

    class Test(Factory):
        TestRegistry = Factory.create_registry(shared=True, post_checks=[])
        ForcedCreditRegistry = Factory.create_registry(shared=True, post_checks=[])

    def test_instantiation(self):
        """Test creating a new method with the abstract methods."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                pass

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                pass

        TestCustomPostCheck()

    def test_wrong_instantiation(self):
        """Test creating a new method without the abstract methods."""

        class TestCustomPostCheck(AbstractPostCheck):
            pass

        with pytest.raises(TypeError):
            TestCustomPostCheck()

    def test_indexdict_validate_register(self):
        """Test the indexdict with the validate register method."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                pass

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                raise ValueError

        index_dict = IndexDict(post_checks=[TestCustomPostCheck()])

        with pytest.raises(ValueError):
            index_dict["test"] = "test"

    def test_indexdict_validate_call(self):
        """Test the indexdict with the validate call method."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                raise ValueError

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                pass

        index_dict = IndexDict(post_checks=[TestCustomPostCheck()])
        index_dict["test"] = "test"

        with pytest.raises(ValueError):
            index_dict["test"] == "test"

    def test_registry_validate_register(self):
        """Test the registry with the validate register method."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                pass

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                raise ValueError

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, post_checks=[TestCustomPostCheck()])

        with pytest.raises(ValueError):

            @TestFactory.TestRegistry.register("registered")
            def test():
                pass

    def test_registry_validate_call(self):
        """Test the registry with the validate call method."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                raise ValueError

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                pass

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, post_checks=[TestCustomPostCheck()])

        @TestFactory.TestRegistry.register("registered")
        def test():
            pass

        print(TestFactory.TestRegistry.show_choices())

        with pytest.raises(ValueError):
            TestFactory.TestRegistry.get("registered")  # == test

    def test_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                if "test" in kwargs:
                    raise ValueError

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                if "test" in kwargs:
                    raise ValueError

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=False, post_checks=[TestCustomPostCheck()])

        with pytest.raises(ValueError):

            @TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(ValueError):

            @TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            TestFactory.TestRegistry.get("additional_params", test="") == test

    def test_Shared_registry_additional_params(self):
        """Test the registry with the postcheck and additional parameters."""

        class TestCustomPostCheck(AbstractPostCheck):
            def validate_call(self, key: str, **kwargs) -> None:
                if "test" in kwargs:
                    raise ValueError

            def validate_register(self, object: Any, key: str, **kwargs) -> None:
                if "test" in kwargs:
                    raise ValueError

        class TestFactory(Factory):
            TestRegistry = Factory.create_registry(shared=True, post_checks=[TestCustomPostCheck()])

        with pytest.raises(ValueError):

            @TestFactory.TestRegistry.register("additional_params", test="")
            def test():
                pass

        with pytest.raises(ValueError):

            @TestFactory.TestRegistry.register("additional_params")
            def test2():
                pass

            TestFactory.TestRegistry.get("additional_params", test="") == test
