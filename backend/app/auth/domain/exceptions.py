class AuthException(Exception):
    """Base exception for all authentication domain errors."""
    pass

class UserAlreadyExistsError(AuthException):
    """Raised when an attempt is made to register an existing email or username."""
    pass

class InvalidCredentialsError(AuthException):
    """Raised when login fails due to an incorrect email or password."""
    pass

class InactiveUserError(AuthException):
    """Raised when an inactive user attempts to log in."""
    pass
