"""Test cases for Registry factory pattern ensurance.
Author: PeterHartog
"""
import pytest
from abstract_codebase.checks.factory_pattern import FactoryPattern
from abstract_codebase.factory import Factory


class Pattern:
    """Test pattern."""

    def __init__(self, name):
        self.name = name

    def hello_world(self):
        """Hello world."""
        print("Hello world")


class TestFactoryPattern:
    """Test cases for versioning."""

    class TestFactory(Factory):
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

        self.TestFactory.TestRegistry.register_prebuilt(key="pattern_test", obj=Pattern)

    def test_wrong_pattern(self):
        """Test the wrong pattern."""

        with pytest.warns():
            self.TestFactory.TestRegistry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")

        with pytest.raises(Exception):
            self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_pattern_test", obj="wrong_pattern")

    def test_inhereted_pattern(self):
        """Test inhereted pattern."""

        class InheretedPattern(Pattern):
            pass

        class DoubleInheretedPattern(InheretedPattern):
            pass

        self.TestFactory.TestRegistry.register_prebuilt(key="inhereted_test", obj=InheretedPattern)
        self.TestFactory.TestRegistry.register_prebuilt(key="double_inhereted_test", obj=DoubleInheretedPattern)

    def test_wrong_inhereted_pattern(self):
        """Test wrong inhereted pattern."""

        class WrongPattern:
            pass

        with pytest.warns():
            self.TestFactory.TestRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

        with pytest.raises(Exception):
            self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_inhereted_test", obj=WrongPattern)

    def test_common_pattern(self):  # TODO: This shouldn't be a warning, but it is.
        """Test common pattern."""

        class CommonPattern:
            def __init__(self, name):
                self.name = name

            def hello_world(self):
                """Hello world."""
                print("Hello world")

        self.TestFactory.TestRegistry.register_prebuilt(key="common_pattern_test", obj=CommonPattern)

    def test_wrong_common_pattern(self):
        """Test wrong common pattern."""

        class WrongPattern:
            def __init__(self, name):
                self.name = name

            def hello_world2(self):
                """Hello world 2."""
                print("Hello world 2: Electric Boogaloo")

        with pytest.warns():
            self.TestFactory.TestRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)

        with pytest.raises(Exception):
            self.TestFactory.ForcedRegistry.register_prebuilt(key="wrong_common_pattern_test", obj=WrongPattern)

    # def test_forced(self):
    #     """Test the forced versioning."""

    #     with pytest.raises(Exception):

    #         @self.TestFactory.ForcedRegistry.register("test2")
    #         def test2():
    #             pass

    # def test_shared(self):
    #     """Test the shared versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test3", version="0.0.1", date="2020-01-01")
    #     def test3():
    #         pass

    # def test_shared_forced(self):
    #     """Test the shared forced versioning."""

    #     with pytest.raises(Exception):

    #         @self.TestFactory.ForcedSharedRegistry.register("test4")
    #         def test4():
    #             pass

    # def test_get_versioning(self):
    #     """Test the get versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test5", version="0.0.1", date="2020-01-01")
    #     def test5():
    #         pass

    #     self.TestFactory.ForcedSharedRegistry.get("test5", version="0.0.1", date="2020-01-01")

    # def test_get_wrong_versioning(self):
    #     """Test the get wrong versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test6", version="0.0.1", date="2020-01-01")
    #     def test6():
    #         pass

    #     with pytest.raises(Exception):
    #         self.TestFactory.ForcedSharedRegistry.get("test6", version="0.0.2", date="2020-01-01")

    # def test_get_no_versioning(self):
    #     """Test the get no versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test7", version="0.0.1", date="2020-01-01")
    #     def test7():
    #         pass

    #     with pytest.raises(Exception):
    #         self.TestFactory.ForcedSharedRegistry.get("test7")

    # def test_get_incomplete_versioning(self):
    #     """Test the get incomplete versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test8", version="0.0.1", date="2020-01-01")
    #     def test8():
    #         pass

    #     with pytest.raises(Exception):
    #         self.TestFactory.ForcedSharedRegistry.get("test8", version="0.0.1")

    # def test_get_version(self):
    #     """Test the get incomplete versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test9", version="0.0.1", date="2020-01-01")
    #     def test9():
    #         pass

    #     assert self.TestFactory.ForcedSharedRegistry.get_info("test9")["Versioning"]["version"] == "0.0.1"

    # def test_print_version(self):
    #     """Test the get incomplete versioning."""

    #     @self.TestFactory.ForcedSharedRegistry.register("test10", version="0.0.1", date="2020-01-01")
    #     def test10():
    #         pass

    #     assert self.TestFactory.ForcedSharedRegistry.print_info("test10") is None

    # def test_custom_version(self):
    #     """Test custom versioning."""

    #     @dataclass
    #     class CustomFields:
    #         """Custom fields."""

    #         version: str
    #         date: str
    #         environment: str

    #     Registry = Factory.create_registry(shared=True, checks=[Versioning(CustomFields, forced=False)])

    #     @Registry.register("test11", version="0.0.1", date="2020-01-01", environment="test")
    #     def test11():
    #         pass

    #     assert Registry.get_info("test11")["Versioning"]["environment"] == "test"
