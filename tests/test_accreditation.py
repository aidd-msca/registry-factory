"""Test cases for the accreditation module.
Author: all hail Github Copilot (untested)
"""
from abstract_codebase.accreditation import Accreditation, CreditInfo, CreditType


class TestAccreditation:
    """Test cases for the Accreditation class."""

    def test_add_credit(self):
        """Test the add_credit method."""
        accreditation = Accreditation()
        accreditation.add_credit(
            "test", CreditInfo("test", "test", "test", "test"), CreditType.REFERENCE,
        )
        assert accreditation.accreditations["test"] == (
            CreditInfo("test", "test", "test", "test"),
            CreditType.REFERENCE,
        )

    def test_get(self):
        """Test the get method."""
        accreditation = Accreditation()
        accreditation.add_credit(
            "test", CreditInfo("test", "test", "test", "test"), CreditType.REFERENCE,
        )
        assert accreditation.get("test") == (CreditInfo("test", "test", "test", "test"), CreditType.REFERENCE,)

    def test_register_accreditation(self):
        """Test the register_accreditation method."""
        accreditation = Accreditation()
        accreditation.add_credit(
            "test", CreditInfo("test", "test", "test", "test"), CreditType.REFERENCE,
        )
        accreditation.register_accreditation("test")
        assert accreditation.called_objects == {"test"}

    def test_called(self):
        """Test the called method."""
        accreditation = Accreditation()
        accreditation.add_credit(
            "test", CreditInfo("test", "test", "test", "test"), CreditType.REFERENCE,
        )
        accreditation.called("test")
        assert accreditation.called_objects == {"test"}
