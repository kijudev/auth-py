from app.core.errors import AuthenticationError, ConflictError


class InvalidCredentialsError(AuthenticationError):
    code = "invalid_credentials"
    message = "Invalid email or password"


class EmailAlreadyRegisteredError(ConflictError):
    code = "email_already_registered"
    message = "Email already registered"
