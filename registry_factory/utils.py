"""Utilities for the registry_factory package."""


class RegistrationError(Exception):
    """Registration error."""

    def __init__(self, message: str):
        """Initialize the RegistrationError."""
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the string representation of the RegistrationError."""
        return f"RegistrationError: {self.message}"


class RegistrationWarning(Warning):
    """Registration warning."""

    def __init__(self, message: str):
        """Initialize the RegistrationWarning."""
        super().__init__(message)
        self.message = message

    def __str__(self):
        """Return the string representation of the RegistrationWarning."""
        return f"RegistrationWarning: {self.message}"
