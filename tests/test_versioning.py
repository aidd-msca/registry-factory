"""Test cases for Registry meta information through versioning (other meta modules: accreditation).
Author: PeterHartog
"""
from dataclasses import dataclass

import pytest

from registry_factory.checks.versioning import Versioning
from registry_factory.factory import Factory


class TestVersioning:
    """Test cases for versioning."""

    class _TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=False, checks=[Versioning(forced=False)])
        TestSharedRegistry = Factory.create_registry(shared=True, checks=[Versioning(forced=False)])
        ForcedRegistry = Factory.create_registry(shared=False, checks=[Versioning(forced=True)])
        ForcedSharedRegistry = Factory.create_registry(shared=True, checks=[Versioning(forced=True)])

    def test_versioning(self):
        """Test the versioning."""

        @self._TestFactory.ForcedRegistry.register("test1", version="0.0.1", date="2020-01-01")
        def test1():
            pass

    def test_forced(self):
        """Test the forced versioning."""

        with pytest.raises(Exception):

            @self._TestFactory.ForcedRegistry.register("test2")
            def test2():
                pass

    def test_shared(self):
        """Test the shared versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test3", version="0.0.1", date="2020-01-01")
        def test3():
            pass

    def test_shared_forced(self):
        """Test the shared forced versioning."""

        with pytest.raises(Exception):

            @self._TestFactory.ForcedSharedRegistry.register("test4")
            def test4():
                pass

    def test_get_versioning(self):
        """Test the get versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test5", version="0.0.1", date="2020-01-01")
        def test5():
            pass

        self._TestFactory.ForcedSharedRegistry.get("test5", version="0.0.1", date="2020-01-01")

    def test_get_wrong_versioning(self):
        """Test the get wrong versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test6", version="0.0.1", date="2020-01-01")
        def test6():
            pass

        with pytest.raises(Exception):
            self._TestFactory.ForcedSharedRegistry.get("test6", version="0.0.2", date="2020-01-01")

    def test_get_no_versioning(self):
        """Test the get no versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test7", version="0.0.1", date="2020-01-01")
        def test7():
            pass

        with pytest.raises(Exception):
            self._TestFactory.ForcedSharedRegistry.get("test7")

    def test_get_incomplete_versioning(self):
        """Test the get incomplete versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test8", version="0.0.1", date="2020-01-01")
        def test8():
            pass

        with pytest.raises(Exception):
            self._TestFactory.ForcedSharedRegistry.get("test8", version="0.0.1")

    def test_get_version(self):
        """Test the get incomplete versioning."""

        @self._TestFactory.ForcedSharedRegistry.register("test9", version="0.0.1", date="2020-01-01")
        def test9():
            pass

        assert self._TestFactory.ForcedSharedRegistry.get_info("test9", version="0.0.1")["date"] == "2020-01-01"

    def test_custom_version(self):
        """Test custom versioning."""

        @dataclass
        class CustomFields:
            """Custom fields."""

            version: str
            date: str
            environment: str

        Registry = Factory.create_registry(shared=True, checks=[Versioning(CustomFields, forced=False)])

        @Registry.register("test10", version="0.0.1", date="2020-01-01", environment="test")
        def test10():
            pass

        assert Registry.get_info("test10", version="0.0.1")["environment"] == "test"
