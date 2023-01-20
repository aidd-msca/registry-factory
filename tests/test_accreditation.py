"""Test cases for Registry sharing.
Author: PeterHartog
"""
from abstract_codebase.accreditation import Accreditation
from abstract_codebase.index import IndexDict
from abstract_codebase.postchecks import AccreditationPostCheck
import pytest
from abstract_codebase.registration import Factory


class TestAccreditation:
    """Test cases for shared Registry class."""

    class TestFactory(Factory):
        TestRegistry = Factory.create_registry(shared=False, post_checks=[AccreditationPostCheck(forced=False)])
        TestSharedRegistry = Factory.create_registry(shared=True, post_checks=[AccreditationPostCheck(forced=False)])
        ForcedCreditRegistry = Factory.create_registry(shared=False, post_checks=[AccreditationPostCheck(forced=True)])
        ForcedCreditSharedRegistry = Factory.create_registry(
            shared=True, post_checks=[AccreditationPostCheck(forced=True)]
        )

    def test_unregistered_credit(self):
        """Test the add_credit method."""
        accreditation = Accreditation()
        with pytest.raises(KeyError):
            accreditation.get("test")

    def test_add_credit(self):
        """Test the add_credit method."""
        accreditation = Accreditation()
        accreditation.add_credit(index="test", credit={"author": ("name")}, credit_type="reference")
        assert accreditation.accreditations["test"] == ({"author": ("name")}, "reference")

    def test_get(self):
        """Test the get method."""
        accreditation = Accreditation()
        accreditation.add_credit(index="test2", credit={"author": ("name")}, credit_type="reference")
        assert accreditation.get("test2") == ({"author": ("name")}, "reference")

    def test_indexdict_forced(self):
        """Test the indexdict with the validate call method."""

        index_dict = IndexDict(post_checks=[AccreditationPostCheck(forced=True)])

        with pytest.raises(ValueError):
            index_dict["test"] = "test"

    def test_indexdict_accreditation(self):
        """Test the indexdict with the validate call method."""

        index_dict = IndexDict(post_checks=[AccreditationPostCheck(forced=False)])
        index_dict.__setitem__("indextest", "test", credit={"author": ("name")}, credit_type="reference")

        accreditation = Accreditation()
        assert accreditation.get("indextest") == ({"author": ("name")}, "reference")

    def test_register_accreditation(self):
        """Test accreditation through the register method."""

        @self.TestFactory.ForcedCreditRegistry.register("test3", credit={"author": ("name")}, credit_type="reference")
        def test():
            pass

        accreditation = Accreditation()
        assert accreditation.get("test3") == ({"author": ("name")}, "reference")
        assert self.TestFactory.accreditation.get("test3") == ({"author": ("name")}, "reference")
        assert self.TestFactory.TestRegistry.accreditation.get("test3") == ({"author": ("name")}, "reference")

    def test_sharedregister_accreditation(self):
        """Test accreditation through the register method."""

        @self.TestFactory.TestSharedRegistry.register("test4", credit={"author": ("name")}, credit_type="reference")
        def test():
            pass

        accreditation = Accreditation()
        print(dir(self.TestFactory.TestRegistry.index))
        print(self.TestFactory.TestSharedRegistry.show_choices())
        print(accreditation.accreditations)
        print(self.TestFactory.TestSharedRegistry.index.post_checks)
        assert accreditation.get("test4") == ({"author": ("name")}, "reference")
        assert self.TestFactory.accreditation.get("test4") == ({"author": ("name")}, "reference")
        assert self.TestFactory.TestSharedRegistry.accreditation.get("test4") == ({"author": ("name")}, "reference")

    def test_called(self):
        """Test the called method."""

        @self.TestFactory.TestRegistry.register("test5", credit={"author": ("name")}, credit_type="reference")
        def test():
            pass

        accreditation = Accreditation()
        self.TestFactory.TestRegistry.get("test5")
        assert accreditation.called_objects == {"test5"}

    def test_called_shared(self):
        """Test the called method."""

        @self.TestFactory.TestSharedRegistry.register("test6", credit={"author": ("name")}, credit_type="reference")
        def test():
            pass

        accreditation = Accreditation()
        self.TestFactory.TestSharedRegistry.get("test6")
        assert "test6" in accreditation.called_objects

    def test_not_called(self):
        """Test the called method."""

        @self.TestFactory.TestRegistry.register("test7", credit={"author": ("name")}, credit_type="reference")
        def test():
            pass

        accreditation = Accreditation()
        assert "test7" not in accreditation.called_objects
